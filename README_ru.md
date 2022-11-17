<div align="center">

Русский | [English](README.md)

</div>


## Введение

Sevimon это программа с открытым исходным кодом написанная на питоне. Позволяет отслеживать напряжение лицевых мышц через видеокамеру, что может быть использовано для устранения перенапряжения, косвенного воздействия на настроение и, при длительном применении, предотвращения появляния мимических морщин.

Sevimon работает следующим образом: сначала на изображении определяется лицо, затем лицо сопоставляется с каждой из восьми эмоций (злость, презрение, отвращение, страх, радость, отсутствие эмоций, грусть, удивление), после чего для каждой эмоции даётся некая оценка похожести.

Полученные значения сохраняются в журнале в текстовом формате для последующего анализа программой sevistat.
Кроме того, для каждой эмоции в файле настроек можно задать верхние и нижние границы значений, при пересечении которых выдаётся напоминание.

При первом запуске скачиваются модели, после чего программа не требует подключения к интернету.

## Непосредственный запуск программы
### Linux/UNIX

Поставьте следующие пакеты средствами дистрибутива: git, python, python-pip.
Скачайте проект, установите зависимости, которых не хватает в системе:
```shell
git clone https://github.com/ioctl-user/sevimon.git
cd sevimon
python3 -m pip install -r requirements.txt
```

Для запуска используйте команду `sevimon.py` из папки проекта.
Для отображения статистики используйте команду `sevistat.py` из папки проекта. Должно быть накоплено хотя бы 2 часа статистики для её показа.

При первом запуске скачиваются модели, создаются конфигурационный файл ~/.config/sevimon/sevimon.cfg, который можно редактировать при необходимости.
Журнал эмоций пишется в папку ~/.cache/sevimon/log/ .

### Windows 

Установите пакет [python вместе со встроенным pip](https://www.python.org/downloads/windows/).
Установите пакет [git](https://git-scm.com/download/win).

Запустите Powershell, набрав комбинацию клавиш Win+X и выбрав запуск от обычного пользователя.

Введите следующие команды для скачивания пакета и установки зависимостей:
```shell
git clone https://github.com/ioctl-user/sevimon.git
cd sevimon
python3 -m pip install -r requirements.txt
```

Для запуска используйте команду `python.exe -m sevimon.py` из папки проекта.
Для отображения статистики используйте команду `python.exe -m sevistat.py` из папки проекта. Должно быть накоплено хотя бы 2 часа статистики для её показа.
При первом запуске скачиваются модели, создаются редактируемый конфигурационный файл sevimon.cfg и папка для журнала эмоций.

В случе нехватки модулей DLL, установите [MS Visual C](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist).

## Запуск через Docker в Linux
Программа sevimon запускается следующим образом:
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
Программа sevistat запускается следующим образом:
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

## Лицензия файлов проекта

AGPLv3

## Благодарности

Для поиска лиц на изображения используются наработки проекта [Centerface](https://github.com/Star-Clouds/CenterFace/blob/master/prj-python/).
Для определения эмоций используется проект [HSEmotion](https://github.com/HSE-asavchenko/face-emotion-recognition).
