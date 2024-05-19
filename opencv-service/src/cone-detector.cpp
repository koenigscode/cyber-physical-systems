#include "cluon-complete.hpp"
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "cone-detector.hpp"

// define the color thresholds
const cv::Scalar lowerYellow(20, 100, 100), upperYellow(30, 255, 255);
const cv::Scalar lowerBlue(100, 150, 50), upperBlue(140, 255, 150);

std::vector<std::vector<cv::Point>> detectCones(cv::Mat &frame,
                                                const cv::Scalar &lowerColor,
                                                const cv::Scalar &upperColor) {
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

std::vector<std::vector<cv::Point>> detectYellowCones(cv::Mat &frame) {
  return detectCones(frame, lowerYellow, upperYellow);
}

std::vector<std::vector<cv::Point>> detectBlueCones(cv::Mat &frame) {
  return detectCones(frame, lowerBlue, upperBlue);
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

std::vector<cv::Point2f> getYellowMassCenters(cv::Mat &frame) {

  return getMassCenters(detectYellowCones(frame));
};

std::vector<cv::Point2f> getBlueMassCenters(cv::Mat &frame) {

  return getMassCenters(detectBlueCones(frame));
};
