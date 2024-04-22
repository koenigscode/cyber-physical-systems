cmake_minimum_required(VERSION 3.2)
project(helloworld)
set(CMAKE_CXX_STANDARD 11)
add_executable(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/src/helloworld.cpp ${CMAKE_CURRENT_SOURCE_DIR}/src/PrimeChecker.cpp)

# Testing
enable_testing()
add_executable(${PROJECT_NAME}-Runner src/TestPrimeChecker.cpp ${CMAKE_CURRENT_SOURCE_DIR}/src/PrimeChecker.cpp)
add_test(NAME ${PROJECT_NAME}-Runner COMMAND ${PROJECT_NAME}-Runner)

# set compiler flags
set(CMAKE_CXX_FLAGS "-O0 --coverage")

# find required tools
find_program(GCOVR gcovr REQUIRED)

# add coverage target
add_custom_target(coverage
  COMMAND ${CMAKE_MAKE_PROGRAM} test
  COMMAND ${GCOVR} -r .. --xml-pretty -e ".*\.hpp" -e ".*Test.*" --exclude-unreachable-branches -o coverage.xml
  COMMAND ${GCOVR} -r .. -e ".*\.hpp" -e ".*Test.*" --exclude-unreachable-branches

  WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
