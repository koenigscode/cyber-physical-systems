# Based on Dockerfile from Christian Berger in A5

##################################################
# Section 1: Build the application
FROM ubuntu:22.04 as builder

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

RUN apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    ca-certificates \
    wget

ADD . /opt/sources
WORKDIR /opt/sources

# Download catch, enter build folder
RUN cd /opt/sources && \
    cd ./src/tests && \
    wget https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp && \
    cd ../.. && \
    cp src/tests/* src/ && \
    mkdir -p build && \
    cd build

# Build using cmake + make
RUN cd build && \ 
    cmake -D CMAKE_BUILD_TYPE=Release .. && \
    make && make test && cp helloworld /tmp

##################################################
# Section 2: Bundle the application.
FROM ubuntu:22.04
MAINTAINER Christian Berger christian.berger@gu.se

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

WORKDIR /opt
COPY --from=builder /tmp/helloworld .
ENTRYPOINT ["/opt/helloworld"]
