# Based on Dockerfile from Christian Berger in A5

##################################################
# Section 1: Build the application
FROM ubuntu:22.04 as builder

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y --no-install-recommends \
    cmake \
    lcov \
    build-essential \
    ca-certificates \
    python3 python3-distutils \
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
    cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_COVERAGE=true .. && \
    make && make test && make coverage && lcov --list coverage.info > lcov.out && python3 ../lcov_cobertura.py coverage.info && cp helloworld coverage/index.html coverage.info lcov.out coverage.xml /tmp

##################################################
# Section 2: Bundle the application.
FROM ubuntu:22.04 as runner
MAINTAINER Christian Berger christian.berger@gu.se

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y

WORKDIR /opt
COPY --from=builder /tmp/helloworld .
COPY --from=builder /tmp/index.html .
COPY --from=builder /tmp/coverage.info .
COPY --from=builder /tmp/coverage.xml .
COPY --from=builder /tmp/lcov.out .
ENTRYPOINT ["/bin/sh"]

FROM scratch as copytohost
COPY --from=builder /tmp/coverage.xml .

