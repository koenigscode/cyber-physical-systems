/*
 * Copyright (C) 2020  Christian Berger
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

// Include the single-file, header-only middleware libcluon to create
// high-performance microservices
#include "cluon-complete.hpp"
// Include the OpenDLV Standard Message Set that contains messages that are
// usually exchanged for automotive or robotic applications
#include "opendlv-standard-message-set.hpp"

// Include the GUI and image processing header files from OpenCV
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <onnxruntime_cxx_api.h>

#include <cmath>
#include <deque>
#include <iostream>
#include <mutex>
#include <ostream>
#include <string>
#include <vector>

class CurrentPerformanceChecker {
private:
  std::deque<bool> within_threshold;
  size_t capacity;

public:
  CurrentPerformanceChecker(size_t capacity) : capacity(capacity) {}

  void add(bool value) {
    within_threshold.push_back(value);
    if (within_threshold.size() > capacity) {
      within_threshold.pop_front();
    }
  }

  size_t getSize() { return capacity; }

  float getPercentage() const {
    size_t trueCount = 0;
    for (bool val : within_threshold) {
      if (val) {
        trueCount++;
      }
    }
    return static_cast<float>(trueCount) / within_threshold.size();
  }
};

bool isWithinPercentThreshold(float target, float prediction,
                              float percentage) {
  float threshold = std::abs(target * percentage);
  float diff = std::abs(target - prediction);

  return diff <= threshold;
}

// dectecting and drawing conical object
std::vector<std::vector<cv::Point>> detectCones(cv::Mat &frame,
                                                const cv::Scalar &lowerColor,
                                                const cv::Scalar &upperColor,
                                                const cv::Scalar &drawColor) {
  // convert to HSV color empty
  cv::Mat hsv;
  cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

  // create the color mask
  cv::Mat mask;
  cv::inRange(hsv, lowerColor, upperColor, mask);

  // find contours in the mask
  std::vector<std::vector<cv::Point>> contours;
  cv::findContours(mask, contours, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE,
                   cv::Point(0, 0));

  return contours;
}

std::vector<cv::Point2f>
getMassCenters(std::vector<std::vector<cv::Point>> contours) {

  const float CLUSTER_RANGE = 25.0;

  std::vector<cv::Point2f> massCenters(contours.size());
  cv::Point2f massCenter;
  cv::Point2f prevMassCenter;

  unsigned int counter = 0;

  for (auto &contour : contours) {

    // Getting the moments
    cv::Moments yellowMoments = cv::moments(contour, false);
    // Check to avoid dividing by zero
    if (yellowMoments.m00 != 0) {
      // Mass centers
      massCenter = cv::Point2f(yellowMoments.m10 / yellowMoments.m00,
                               yellowMoments.m01 / yellowMoments.m00);
      // Do no add trash values
      if (massCenter.y != 0 && massCenter.x != 0) {
        // Prevent out of index out of bounds errors
        if (counter > 0) {
          // Compare the current mass center to the previous one to see if it is
          // in the same cone
          if (std::abs(massCenter.y - prevMassCenter.y) > CLUSTER_RANGE &&
              std::abs(massCenter.x - prevMassCenter.x) > CLUSTER_RANGE) {
            // Only add the mass center to our list if it is on a different cone
            massCenters.push_back(massCenter);
          }
        } else {
          // Initial loop
          massCenters.push_back(massCenter);
        }
      }
      // Remember previous massCenter
      prevMassCenter = massCenter;
    }
    counter++;
  }

  return massCenters;
}

int32_t main(int32_t argc, char **argv) {
  int32_t retCode{1};
  // Parse the command line parameters as we require the user to specify some
  // mandatory information on startup.
  auto commandlineArguments = cluon::getCommandlineArguments(argc, argv);
  if ((0 == commandlineArguments.count("cid")) ||
      (0 == commandlineArguments.count("name")) ||
      (0 == commandlineArguments.count("width")) ||
      (0 == commandlineArguments.count("height"))) {
    std::cerr << argv[0]
              << " attaches to a shared memory area containing an ARGB image."
              << std::endl;
    std::cerr << "Usage:   " << argv[0]
              << " --cid=<OD4 session> --name=<name of shared memory area> "
                 "[--verbose]"
              << std::endl;
    std::cerr << "         --cid:    CID of the OD4Session to send and receive "
                 "messages"
              << std::endl;
    std::cerr << "         --name:   name of the shared memory area to attach"
              << std::endl;
    std::cerr << "         --width:  width of the frame" << std::endl;
    std::cerr << "         --height: height of the frame" << std::endl;
    std::cerr << "Example: " << argv[0]
              << " --cid=253 --name=img --width=640 --height=480 --verbose"
              << std::endl;
  } else {
    // Extract the values from the command line parameters
    const std::string NAME{commandlineArguments["name"]};
    const uint32_t WIDTH{
        static_cast<uint32_t>(std::stoi(commandlineArguments["width"]))};
    const uint32_t HEIGHT{
        static_cast<uint32_t>(std::stoi(commandlineArguments["height"]))};
    const bool VERBOSE{commandlineArguments.count("verbose") != 0};

    // define the color threshould here
    const cv::Scalar lowerYellow(20, 100, 100), upperYellow(30, 255, 255);
    const cv::Scalar lowerBlue(100, 150, 50), upperBlue(140, 255, 150);

    // Attach to the shared memory.
    std::unique_ptr<cluon::SharedMemory> sharedMemory{
        new cluon::SharedMemory{NAME}};
    if (sharedMemory && sharedMemory->valid()) {
      std::clog << argv[0] << ": Attached to shared memory '"
                << sharedMemory->name() << " (" << sharedMemory->size()
                << " bytes)." << std::endl;

      // Interface to a running OpenDaVINCI session where network messages are
      // exchanged. The instance od4 allows you to send and receive messages.
      cluon::OD4Session od4{
          static_cast<uint16_t>(std::stoi(commandlineArguments["cid"]))};

      opendlv::proxy::GroundSteeringRequest gsr;
      std::mutex gsrMutex;
      auto onGroundSteeringRequest = [&gsr,
                                      &gsrMutex](cluon::data::Envelope &&env) {
        // The envelope data structure provide further details, such as
        // sampleTimePoint as shown in this test case:
        // https://github.com/chrberger/libcluon/blob/master/libcluon/testsuites/TestEnvelopeConverter.cpp#L31-L40
        std::lock_guard<std::mutex> lck(gsrMutex);
        gsr = cluon::extractMessage<opendlv::proxy::GroundSteeringRequest>(
            std::move(env));
      };

      od4.dataTrigger(opendlv::proxy::GroundSteeringRequest::ID(),
                      onGroundSteeringRequest);

      opendlv::proxy::AngularVelocityReading angularV;
      std::mutex angularVMutex;
      auto onAngularVRequest = [&angularV,
                                &angularVMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(angularVMutex);
        angularV =
            cluon::extractMessage<opendlv::proxy::AngularVelocityReading>(
                std::move(env));
      };

      od4.dataTrigger(opendlv::proxy::AngularVelocityReading::ID(),
                      onAngularVRequest);

      opendlv::proxy::AccelerationReading accel;
      std::mutex accelMutex;
      auto onAccelRequest = [&accel, &accelMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(accelMutex);
        accel = cluon::extractMessage<opendlv::proxy::AccelerationReading>(
            std::move(env));
      };

      od4.dataTrigger(opendlv::proxy::AccelerationReading::ID(),
                      onAccelRequest);

      opendlv::proxy::VoltageReading voltage;
      std::mutex voltageMutex;
      auto onVoltageRequest = [&voltage,
                               &voltageMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(voltageMutex);
        voltage = cluon::extractMessage<opendlv::proxy::VoltageReading>(
            std::move(env));
      };

      od4.dataTrigger(opendlv::proxy::VoltageReading::ID(), onVoltageRequest);

      opendlv::proxy::PedalPositionReading pedal;
      std::mutex pedalMutex;
      auto onPedalRequest = [&pedal, &pedalMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(pedalMutex);
        pedal = cluon::extractMessage<opendlv::proxy::PedalPositionReading>(
            std::move(env));
      };

      od4.dataTrigger(opendlv::proxy::PedalPositionReading::ID(),
                      onPedalRequest);

      opendlv::proxy::MagneticFieldReading mag;
      std::mutex magMutex;
      auto onMagneticFieldReading = [&mag,
                                     &magMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(magMutex);
        mag = cluon::extractMessage<opendlv::proxy::MagneticFieldReading>(
            std::move(env));
      };

      od4.dataTrigger(opendlv::proxy::PedalPositionReading::ID(),
                      onPedalRequest);

      std::string model_path = "./clr.onnx";
      Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "InferenceEnv");
      Ort::SessionOptions session_options;
      Ort::Session session(env, model_path.c_str(), session_options);

      std::vector<const char *> input_node_names = {"X"};
      std::vector<const char *> output_node_names = {"variable"};

      Ort::MemoryInfo memory_info =
          Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeDefault);

      int frames_processed{0};
      int frames_within_threshold{0};

      CurrentPerformanceChecker perfChecker(20);

      // Endless loop; end the program by pressing Ctrl-C.
      while (od4.isRunning()) {
        // OpenCV data structure to hold an image.
        cv::Mat fullImg;
        cv::Mat img;

        // Wait for a notification of a new frame.
        sharedMemory->wait();

        // Lock the shared memory.
        sharedMemory->lock();
        {
          // Copy the pixels from the shared memory into our own data
          // structure.
          cv::Mat wrapped(HEIGHT, WIDTH, CV_8UC4, sharedMemory->data());
          fullImg = wrapped.clone();
          img = fullImg(cv::Rect(0, HEIGHT / 2, WIDTH, HEIGHT / 2));

          // create a black rectangle
          cv::rectangle(img, cv::Point(220, 140), cv::Point(440, 240),
                        cv::Vec3b(0, 0, 0), cv::FILLED);
        }

        cluon::data::TimeStamp ts = sharedMemory->getTimeStamp().second;
        int64_t ts_micro = cluon::time::toMicroseconds(ts);

        sharedMemory->unlock();

        // Get countours of the yellow cones
        std::vector<std::vector<cv::Point>> yellowContours =
            detectCones(img, lowerYellow, upperYellow, cv::Scalar(0, 255, 255));

        // Get countours of the blue cones
        std::vector<std::vector<cv::Point>> blueContours =
            detectCones(img, lowerBlue, upperBlue, cv::Scalar(255, 0, 0));

        // Get mass centers of the yellow cones
        std::vector<cv::Point2f> yellowMassCenters =
            getMassCenters(yellowContours);

        // Get mass centers of the blue cones
        std::vector<cv::Point2f> blueMassCenters =
            getMassCenters(blueContours);

        // For each mass center add a circle to the image
        for (auto massCenter : yellowMassCenters) {
          cv::circle(img, massCenter, 5, cv::Scalar(0, 255, 0), -1);
        }

        // For each mass center add a circle to the image
        for (auto massCenter : blueMassCenters) {
          cv::circle(img, massCenter, 5, cv::Scalar(0, 255, 0), -1);
        }

        // If you want to access the latest received ground steering, don't
        // forget to lock the mutex:
        {
          std::lock_guard<std::mutex> gsrLock(gsrMutex);
          std::lock_guard<std::mutex> angularVLock(angularVMutex);
          std::lock_guard<std::mutex> accelLock(accelMutex);
          std::lock_guard<std::mutex> voltageLock(voltageMutex);
          std::lock_guard<std::mutex> pedalLock(pedalMutex);
          std::lock_guard<std::mutex> magLock(magMutex);

          std::cout << "groundSteering = " << gsr.groundSteering() << ";";
          if (VERBOSE) {
            // Store cone coordinates (mass centers)
            std::string yellow;
            std::string blue;

            // Count how many cones we detected
            unsigned int yellowCounter = 0;
            unsigned int blueCounter = 0;
            unsigned int totalCounter = 0;

            // Iterate through the detected yellow cones
            for (auto massCenter : yellowMassCenters) {
              // Avoid printing trash values
              if (massCenter.x != 0 && totalCounter < 2) {
                yellow = yellow + std::to_string(massCenter.x) + ";" +
                         std::to_string(massCenter.y) + ";";
                yellowCounter++;
                totalCounter++;
              }
            }
            // Iterate through the detected blue cones
            for (auto massCenter : blueMassCenters) {
              // Avoid printing trash values
              if (massCenter.x != 0 && totalCounter < 2) {
                blue = blue + std::to_string(massCenter.x) + ";" +
                       std::to_string(massCenter.y) + ";";
                blueCounter++;
                totalCounter++;
              }
            }

            while (totalCounter < 2) {
              blue = blue + "NaN;NaN;";
              totalCounter++;
            }

            std::cout << std::to_string(ts_micro / 1000000) << ";"
                      << std::to_string(ts_micro % 1000000) << ";";

            std::cout << yellow;
            std::cout << blue;
            std::cout << std::endl;
          }
        }

        std::vector<float> input_data = {
            angularV.angularVelocityX(), angularV.angularVelocityY(),
            angularV.angularVelocityZ(), accel.accelerationX(),
            accel.accelerationY(),       accel.accelerationZ(),
            voltage.voltage(),           pedal.position(),
            mag.magneticFieldX(),        mag.magneticFieldY(),
            mag.magneticFieldZ()};

        std::vector<int64_t> input_shape = {1, input_data.size()};

        Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
            memory_info, input_data.data(), input_data.size(),
            input_shape.data(), input_shape.size());

        std::vector<Ort::Value> input_tensors;
        input_tensors.push_back(std::move(input_tensor));

        auto output_tensors =
            session.Run(Ort::RunOptions{nullptr}, input_node_names.data(),
                        input_tensors.data(), input_tensors.size(),
                        output_node_names.data(), 1);

        float *output_data = output_tensors[0].GetTensorMutableData<float>();

        float prediction = output_data[0];
        if (prediction > 0.22) {
          prediction = 0.22;
        } else if (prediction < -0.22) {
          prediction = -0.22;
        }

        if (gsr.groundSteering() != 0) {
          bool isWithinThreshold =
              isWithinPercentThreshold(gsr.groundSteering(), prediction, 0.25);

          perfChecker.add(isWithinThreshold);
          frames_processed++;
          frames_within_threshold += isWithinThreshold;
        }

        std::cout << "group_22;" << std::to_string(ts_micro) << ";"
                  << prediction << std::endl;

        cv::putText(
            img,
            "Average correct: " +
                std::to_string(static_cast<float>(frames_within_threshold) /
                               frames_processed * 100.0) +
                "%",
            cv::Point(10, 10), cv::FONT_HERSHEY_DUPLEX, 0.5, CV_RGB(255, 0, 0),
            1);

        cv::putText(img,
                    "Correct within last " +
                        std::to_string(perfChecker.getSize()) + " frames: " +
                        std::to_string(perfChecker.getPercentage() * 100.0) +
                        "%",
                    cv::Point(10, 30), cv::FONT_HERSHEY_DUPLEX, 0.5,
                    CV_RGB(255, 0, 0), 1);

        cv::putText(img, "Prediction: " + std::to_string(prediction),
                    cv::Point(10, 60), cv::FONT_HERSHEY_DUPLEX, 0.5,
                    CV_RGB(255, 0, 0), 1);

        if (VERBOSE) {
          cv::imshow(sharedMemory->name().c_str(), img);
          cv::waitKey(1);

          std::cout << "actual;" << std::to_string(ts_micro) << ";"
                    << std::to_string(gsr.groundSteering()) << std::endl;

          std::cout << "% correct: "
                    << std::to_string(
                           static_cast<float>(frames_within_threshold) /
                           frames_processed * 100.0)
                    << "%" << std::endl;
        }
      }
    }
    retCode = 0;
  }
  return retCode;
}
