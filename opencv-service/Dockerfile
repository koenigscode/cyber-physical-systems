# Copyright (C) 2020  Christian Berger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# First stage for building the software:
FROM registry.git.chalmers.se/courses/dit638/students/2024-group-22/ubuntu as builder
MAINTAINER Christian Berger "christian.berger@gu.se"

ENV DEBIAN_FRONTEND noninteractive

# Upgrade the Ubuntu 18.04 LTS base image
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

# Install the development libraries for OpenCV
RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    cmake \
    build-essential \
    libopencv-dev \
    gcovr \
    python3 python3-pip \
    wget 

RUN apt install python3-setuptools

ARG TARGETPLATFORM

COPY ./lib/onnxruntime /usr/onnxruntime

RUN echo "Building for ${TARGETPLATFORM}"


ADD . /opt/sources
WORKDIR /opt/sources

RUN mkdir -p /usr/onnxruntime/include/
RUN mkdir -p /usr/onnxruntime/lib/

RUN if [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
    mv /usr/onnxruntime/arm64/lib/* /usr/onnxruntime/lib/; \
    mv /usr/onnxruntime/arm64/include/* /usr/onnxruntime/include/; \
    elif [ "${TARGETPLATFORM}" = "linux/arm/v7" ]; then \
    mv /usr/onnxruntime/arm32/lib/* /usr/onnxruntime/lib/; \
    mv /usr/onnxruntime/arm32/include/* /usr/onnxruntime/include/; \
    else \
    mv /usr/onnxruntime/amd/lib/* /usr/onnxruntime/lib/; \
    mv /usr/onnxruntime/amd/include/* /usr/onnxruntime/include/; \
    fi

RUN ldconfig /usr/onnxruntime/lib/

RUN cd /opt/sources && \
    cd ./tests && \
    wget https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp && \
    cd .. && \
    cp tests/* src/ && \
    mkdir -p build

RUN cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/tmp .. && \
    make && make install && make test && make coverage && cp coverage.xml /tmp

FROM scratch as copytohost
COPY --from=builder /tmp/coverage.xml .

# Second stage for packaging the software into a software bundle:
FROM registry.git.chalmers.se/courses/dit638/students/2024-group-22/ubuntu
MAINTAINER Christian Berger "christian.berger@gu.se"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

RUN apt-get install -y --fix-missing --no-install-recommends \
    libopencv-core406t64 \
    libopencv-highgui406t64 \
    libopencv-imgproc406t64 

COPY --from=builder /usr/onnxruntime /usr/onnxruntime

RUN ldconfig /usr/onnxruntime/lib

WORKDIR /usr/bin
COPY --from=builder /tmp/bin/opencv-service .
COPY --from=builder /opt/sources/lib/models .
# This is the entrypoint when starting the Docker container; hence, this Docker image is automatically starting our software on its creation
ENTRYPOINT ["/usr/bin/opencv-service"]
