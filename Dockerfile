# Build command: docker build . -t ioctl2/sevimon --no-cache --network=host
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

# Note: language pack is indirectly used for the program localization
RUN apt update && apt install -qq -y --no-install-recommends \
	vim git python3-pip libopencv-dev x11-utils net-tools python3-tk \
	language-pack-ru

RUN ln -sf /bin/bash /bin/sh
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Install package. Need dry run to download all dependencies
RUN pip install git+https://github.com/ioctl-user/sevimon.git && sevimon
