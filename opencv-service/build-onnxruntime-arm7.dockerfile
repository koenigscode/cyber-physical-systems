# Since onnxruntime is not prebuilt for arm32 ("linux/arm/v7"),
# we have to build it manually (sadly)
# Based on build instructions from https://onnxruntime.ai/docs/build/inferencing.html
FROM arm32v7/ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

# Install necessary packages
RUN apt-get update -y && apt-get install -y \
    git \
    build-essential \
    cmake \
    python3-dev \
    python3-pip \
    wget \
    ca-certificates

# Remove the default cmake installation (if any)
RUN apt-get remove -y --purge --auto-remove cmake

# Download and install CMake 3.27
RUN wget -qO- "https://cmake.org/files/v3.27/cmake-3.27.0-Linux-armv7.tar.gz" | tar --strip-components=1 -xz -C /usr/local

# Verify cmake version
RUN cmake --version

# Clone the Onnxruntime repository
RUN git clone --recursive https://github.com/microsoft/onnxruntime.git /onnxruntime

# Set working directory
WORKDIR /onnxruntime



# RUN ./build.sh --config RelWithDebInfo --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --allow_running_as_root
RUN ./build.sh --config RelWithDebInfo --build_shared_lib --parallel --skip_submodule_sync --allow_running_as_root
# RUN ./build.sh --config RelWithDebInfo --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync
# RUN ./build.sh --config RelWithDebInfo --build_shared_lib --parallel --compile_no_warning_as_error --allow_running_as_root --skip_submodule_sync --cmake_extra_defines CMAKE_OSX_ARCHITECTURES=x86_64




# Set environment variables (if needed)
# ENV LD_LIBRARY_PATH /onnxruntime/build/Linux/RelWithDebInfo/

# Define entrypoint or default command (if applicable)
# ENTRYPOINT ["/bin/bash"]

# Optionally, clean up unnecessary files to reduce image size
# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Specify the user when running the container (if needed)
# USER myuser

# Example usage:
# docker build -t onnxruntime-armv7 .
# docker run -it --rm onnxruntime-armv7

