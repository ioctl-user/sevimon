<div align="center">

[Русский](README_ru.md) | English

</div>


## Introduction

Sevimon is an open source program written in Python. It allows facial muscle tension to be monitored through a video camera, which can be used to eliminate stress, indirectly influence mood and, with long-term use, prevent the appearance of facial wrinkles.

Sevimon works by first identifying a face on an image and then comparing it to each of eight emotions (anger, contempt, disgust, fear, joy, no emotion, sadness, surprise), and then giving each emotion some kind of similarity rating.

The values obtained are stored in the logbook in text format for later analysis by the sevistat program.
In addition, for each emotion in the settings file, you can set the upper and lower limits of values, at the crossing of which a reminder is issued.

At the first start-up the models are downloaded, after which the programme does not require an internet connection.

## Direct program startup
## Linux/UNIX

Install the following packages from the distribution: git, python, python-pip.
Download the project, install the dependencies that are missing in the system:
```shell
git clone https://github.com/ioctl-user/sevimon.git
cd sevimon
pip install -r  requirements.txt
```

Use the command `sevimon.py` from the project folder to run it.
To display statistics, use the command `sevistat.py` from the project folder. Currently at least two ours of stat needed.

At first startup, models are downloaded, a configuration file ~/.config/sevimon/sevimon.cfg is created, which can be edited if necessary.
The emotion log is written to the ~/.cache/sevimon/log/ .

### Windows 

Install package [python with built-in pip](https://www.python.org/downloads/windows/).
Install [git package](https://git-scm.com/download/win).

Run Powershell by typing Win+X and select userland mode.

Enter the following commands to download the package and install the dependencies:
```shell
git clone https://github.com/ioctl-user/sevimon.git
cd sevimon
pip install -r requirements.txt
```

Use the command `python.exe -m sevimon.py` from the project folder to run it.
Use the command `python.exe -m sevistat.py` from the project folder to display the statistics. Currently at least two ours of stat needed.
The first run downloads the models, creates an editable configuration file sevimon.cfg and a folder for the emotion log.

In case of lack of DLL modules, install [MS Visual C](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist).

## Run via Docker in Linux
The sevimon program is started as follows:
```shell
xhost +localhost
mkdir -p ~/.cache/sevimon/log/
mkdir -p ~/.config/sevimon/
echo > ~/.config/sevimon/sevimon.cfg
docker run -it --rm --privileged \
    --net=none \
    -w /sevimon/ \
    -e DISPLAY=$DISPLAY \
    -e LANG=$LANG \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v $HOME/.config/sevimon/sevimon.cfg:/root/.config/sevimon/sevimon.cfg \
    -v $HOME/.cache/sevimon/log:/root/.cache/sevimon/log \
    -v /dev/video0:/dev/video0 \
    ioctl2/sevimon /sevimon/sevimon.py
xhost -localhost
```
The sevistat program is started as follows:
```shell
xhost +localhost
docker run -it --rm --privileged \
    --net=none \
    -w /sevimon/ \
    -e DISPLAY=$DISPLAY \
    -e LANG=$LANG \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v $HOME/.config/sevimon/sevimon.cfg:/root/.config/sevimon/sevimon.cfg \
    -v $HOME/.cache/sevimon/log:/root/.cache/sevimon/log \
    ioctl2/sevimon /sevimon/sevistat.py
xhost -localhost
```

## Project file licence

AGPLv3

## Acknowledgements

The [Centerface](https://github.com/Star-Clouds/CenterFace/blob/master/prj-python/) project is used to search for faces in images.
The project [HSEmotion](https://github.com/HSE-asavchenko/face-emotion-recognition) is used for emotion detection.

