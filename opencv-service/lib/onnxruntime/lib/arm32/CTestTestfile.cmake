# CMake generated Testfile for 
# Source directory: /onnxruntime/cmake
# Build directory: /onnxruntime/build/Linux/Release
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test([=[onnxruntime_test_all]=] "/onnxruntime/build/Linux/Release/onnxruntime_test_all" "--gtest_output=xml:/onnxruntime/build/Linux/Release/onnxruntime_test_all.Release.results.xml")
set_tests_properties([=[onnxruntime_test_all]=] PROPERTIES  TIMEOUT "7200" WORKING_DIRECTORY "/onnxruntime/build/Linux/Release" _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;224;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;861;AddTest;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
add_test([=[onnx_test_pytorch_converted]=] "/onnxruntime/build/Linux/Release/onnx_test_runner" "/onnxruntime/build/Linux/Release/_deps/onnx-src/onnx/backend/test/data/pytorch-converted")
set_tests_properties([=[onnx_test_pytorch_converted]=] PROPERTIES  _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;1160;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
add_test([=[onnx_test_pytorch_operator]=] "/onnxruntime/build/Linux/Release/onnx_test_runner" "/onnxruntime/build/Linux/Release/_deps/onnx-src/onnx/backend/test/data/pytorch-operator")
set_tests_properties([=[onnx_test_pytorch_operator]=] PROPERTIES  _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;1162;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
add_test([=[onnxruntime_shared_lib_test]=] "/onnxruntime/build/Linux/Release/onnxruntime_shared_lib_test" "--gtest_output=xml:/onnxruntime/build/Linux/Release/onnxruntime_shared_lib_test.Release.results.xml")
set_tests_properties([=[onnxruntime_shared_lib_test]=] PROPERTIES  TIMEOUT "7200" WORKING_DIRECTORY "/onnxruntime/build/Linux/Release" _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;224;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;1282;AddTest;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
add_test([=[onnxruntime_global_thread_pools_test]=] "/onnxruntime/build/Linux/Release/onnxruntime_global_thread_pools_test" "--gtest_output=xml:/onnxruntime/build/Linux/Release/onnxruntime_global_thread_pools_test.Release.results.xml")
set_tests_properties([=[onnxruntime_global_thread_pools_test]=] PROPERTIES  TIMEOUT "7200" WORKING_DIRECTORY "/onnxruntime/build/Linux/Release" _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;224;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;1320;AddTest;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
add_test([=[onnxruntime_customopregistration_test]=] "/onnxruntime/build/Linux/Release/onnxruntime_customopregistration_test" "--gtest_output=xml:/onnxruntime/build/Linux/Release/onnxruntime_customopregistration_test.Release.results.xml")
set_tests_properties([=[onnxruntime_customopregistration_test]=] PROPERTIES  TIMEOUT "7200" WORKING_DIRECTORY "/onnxruntime/build/Linux/Release" _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;224;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;1585;AddTest;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
add_test([=[onnxruntime_logging_apis_test]=] "/onnxruntime/build/Linux/Release/onnxruntime_logging_apis_test" "--gtest_output=xml:/onnxruntime/build/Linux/Release/onnxruntime_logging_apis_test.Release.results.xml")
set_tests_properties([=[onnxruntime_logging_apis_test]=] PROPERTIES  TIMEOUT "7200" WORKING_DIRECTORY "/onnxruntime/build/Linux/Release" _BACKTRACE_TRIPLES "/onnxruntime/cmake/onnxruntime_unittests.cmake;224;add_test;/onnxruntime/cmake/onnxruntime_unittests.cmake;1706;AddTest;/onnxruntime/cmake/onnxruntime_unittests.cmake;0;;/onnxruntime/cmake/CMakeLists.txt;1759;include;/onnxruntime/cmake/CMakeLists.txt;0;")
subdirs("_deps/abseil_cpp-build")
subdirs("_deps/date-build")
subdirs("_deps/google_nsync-build")
subdirs("_deps/utf8_range-build")
subdirs("_deps/protobuf-build")
subdirs("_deps/nlohmann_json-build")
subdirs("_deps/mp11-build")
subdirs("_deps/re2-build")
subdirs("_deps/gsl-build")
subdirs("_deps/flatbuffers-build")
subdirs("_deps/pytorch_cpuinfo-build")
subdirs("_deps/pytorch_clog-build")
subdirs("_deps/googletest-build")
subdirs("_deps/onnx-build")
