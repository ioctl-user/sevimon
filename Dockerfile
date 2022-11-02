# Build command: docker build . -t ioctl2/sevimon --no-cache --network=host
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt update && apt install -qq -y --no-install-recommends \
	vim git python3-pip libopencv-dev x11-utils net-tools python3-tk

RUN ln -sf /bin/bash /bin/sh
RUN ln -sf /usr/bin/python3 /usr/bin/python

# RUN git clone ...
COPY . /sevimon

# Need dry run to download all dependencies
RUN cd sevimon && pip install --no-cache-dir -r ./requirements.txt && ./sevimon.py
