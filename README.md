<div align="center">

[Русский](README_ru.md) | English

</div>

## Table of contents
**[Introduction](#introduction)**

**[Running in Docker in Linux](#running-in-docker-in-Linux)**

**[Running binary versions on Windows 10 and later](#running-binary-versions-on-Windows-10-and-later)**

**[Install and run universal interpreted versions of programs](#install-and-run-universal-interpreted-versions-of-programs)**

**[Project files license](#project-files-license)**

**[Acknowledgements](#acknowledgements)**

## Introduction

Sevimon is a set of open source programs written in Python. It allows facial muscle tension to be monitored through a video camera, which can be used to eliminate overstretching, indirectly influence mood and, with long-term use, prevent the appearance of facial wrinkles.

The basic `sevimon` program works like this: first a face is identified on an image, then each of the eight emotions (anger, contempt, disgust, fear, happiness, no emotion, sadness, surprise) is given a kind of rating for the facial expression.

The values obtained are stored in the logbook in text format for later analysis by the `sevistat` program.
In addition, for each emotion in the settings file, the upper and lower limits of the values can be set and a reminder is given when these are crossed.
The settings file, whose name is displayed on start-up, can be changed in any text editor, or you can use the `sevicfg` graphical utility to configure it. The default setting is to give a warning when anger and surprise are detected, which corresponds to a frown on the eyebrows and a wrinkled forehead.

The models are downloaded the first time you start, after which an internet connection is not required.

## Running in Docker in Linux
Prepared a Docker image with the program, all its dependencies and models, which runs without access to the network.

The sevimon program is run as follows:
```shell
mkdir -p ~/.cache/sevimon/log/
mkdir -p ~/.config/sevimon/
echo > ~/.config/sevimon/sevimon.cfg
xhost +"local:docker@"
docker run -it --rm --privileged \
    --net=none \
    -e DISPLAY=$DISPLAY \
    -e LANG=$LANG \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v $HOME/.config/sevimon/sevimon.cfg:/root/.config/sevimon/sevimon.cfg \
    -v $HOME/.cache/sevimon/log:/root/.local/state/sevimon/log \
    -v /dev/video0:/dev/video0 \
    ioctl2/sevimon:latest sevimon
xhost -"local:docker@"
```
The sevistat programme is started with a command:
```shell
xhost +"local:docker@"
docker run -it --rm --privileged \
    --net=none \
    -e DISPLAY=$DISPLAY \
    -e LANG=$LANG \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v $HOME/.config/sevimon/sevimon.cfg:/root/.config/sevimon/sevimon.cfg \
    -v $HOME/.cache/sevimon/log:/root/.local/state/sevimon/log \
    ioctl2/sevimon:latest sevistat
xhost -"local:docker@"
```
The sevicfg programme is started as follows:
```shell
xhost +"local:docker@"
docker run -it --rm --privileged \
    --net=none \
    -e DISPLAY=$DISPLAY \
    -e LANG=$LANG \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v $HOME/.config/sevimon/sevimon.cfg:/root/.config/sevimon/sevimon.cfg \
    -v $HOME/.cache/sevimon/log:/root/.local/state/sevimon/log \
    ioctl2/sevimon:latest sevicfg
xhost -"local:docker@"
```

## Running binary versions on Windows 10 and later
Prepared [binary program builds](https://github.com/ioctl-user/sevimon/releases/download/v0.1/sevimon_win10_v0.1.zip) with all its dependencies for Windows (x86\_64). Models are automatically downloaded the first time you run it.

## Install and run universal interpreted versions of programs
### Preparatory steps for Linux/UNIX
Install the python and python-pip packages from the distribution.

### Preparatory steps for Windows 
Install package [python along with built-in pip](https://www.python.org/downloads/windows/).

In case of lack of DLL at startup, install [MS Visual C](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist).

Run Powershell by typing Win+X and selecting to run as a normal user.

### Installation and startup

Install the project with all dependencies:
```shell
python3 -m pip install sevimon
```

Warnings may appear during the process asking to add the executable path to the environment variables - this should be done.

Use the `sevimon` command to start the main program. The first run downloads the models and creates a text configuration file.
You can run the program `sevicfg` to configure it.
Use the command `sevistat` to display statistics. It must have been accumulated for at least 2 hours beforehand.

## Project files licence

AGPL v3 or newer.

## Acknowledgements

The [Centerface] project (https://github.com/Star-Clouds/CenterFace/blob/master/prj-python/) is used to search for faces in an image.
The [HSEmotion] project (https://github.com/HSE-asavchenko/face-emotion-recognition) is used for emotion detection.
