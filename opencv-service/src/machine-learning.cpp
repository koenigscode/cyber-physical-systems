#include "machine-learning.hpp"

#include "cluon-complete.hpp"
#include <onnxruntime_cxx_api.h>

float predict(std::vector<float> input_data) {

  std::string model_path = "./clr.onnx";
  Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "InferenceEnv");
  Ort::SessionOptions session_options;
  Ort::Session session(env, model_path.c_str(), session_options);

  std::vector<const char *> input_node_names = {"X"};
  std::vector<const char *> output_node_names = {"variable"};

  Ort::MemoryInfo memory_info =
      Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeDefault);

  std::vector<int64_t> input_shape = {1, input_data.size()};

  Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
      memory_info, input_data.data(), input_data.size(), input_shape.data(),
      input_shape.size());

  std::vector<Ort::Value> input_tensors;
  input_tensors.push_back(std::move(input_tensor));

  auto output_tensors = session.Run(
      Ort::RunOptions{nullptr}, input_node_names.data(), input_tensors.data(),
      input_tensors.size(), output_node_names.data(), 1);

  float *output_data = output_tensors[0].GetTensorMutableData<float>();

  float prediction = output_data[0];
  if (prediction > 0.22) {
    prediction = 0.22;
  } else if (prediction < -0.22) {
    prediction = -0.22;
  }

  return prediction;
}