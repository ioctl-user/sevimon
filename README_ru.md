<div align="center">

Русский | [English](README.md)

</div>

## Оглавление
**[Введение](#Введение)**

**[Запуск в докере в Linux](#запуск-в-докере-в-linux)**

**[Запуск бинарных версий в Windows 10 и более новых](#запуск-бинарных-версий-в-Windows-10-и-более-новых)**

**[Установка и запуск универсальных интерпретирумых версий программ](#установка-и-запуск-универсальных-интерпретирумых-версий-программ)**

**[Лицензия файлов проекта](#лицензия-файлов-проекта)**

**[Благодарности](#благодарности)**

## Введение

Sevimon это набор программ с открытым исходным кодом, написанных на питоне. Позволяет отслеживать напряжение лицевых мышц через видеокамеру, что может быть использовано для устранения перенапряжения, косвенного воздействия на настроение и, при длительном применении, предотвращения появляния мимических морщин.

Основная программа `sevimon` работает следующим образом: сначала на изображении определяется лицо, затем для выражения лица даётся некая оценка соответствия каждой из восьми эмоций (злость, презрение, отвращение, страх, радость, отсутствие эмоций, грусть, удивление).

Полученные значения сохраняются в журнале в текстовом формате для последующего анализа программой `sevistat`.
Кроме того, для каждой эмоции в файле настроек можно задать верхние и нижние границы значений, при пересечении которых тут же выдаётся напоминание.
Файл настроек, имя которого выводится при старте программы, можно менять в любом текстовом редакторе, или же можно воспользоваться графической утилитой `sevicfg` для настройки. По умолчанию настроена выдача предупреждения при определении злости и удивления, что соответствует нахмуренности бровей и сморщенному лбу.

При первом запуске скачиваются модели, после чего подключение к интернету не требуется.

## Запуск в докере в Linux
Подготовлен образ Docker с программой, всеми её зависимостями и моделями, который запускается без доступа к сети.

Программа sevimon запускается следующим образом:
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
Программа sevistat запускается командой:
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
Программа sevicfg запускается так:
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

## Запуск бинарных версий в Windows 10 и более новых
Подготовлены [бинарные сборки программы](https://github.com/ioctl-user/sevimon/releases/download/v0.1/sevimon_win10_v0.1.zip) со всеми её зависимостями для Windows (x86\_64). Модели автоматически скачиваются при первом запуске.

## Установка и запуск универсальных интерпретирумых версий программ
### Подготовительные действия для Linux/UNIX
Поставьте пакеты python и python-pip средствами дистрибутива.

### Подготовительные действия для Windows 
Установите пакет [python вместе со встроенным pip](https://www.python.org/downloads/windows/).

В случае нехватки DLL при запуске программы, установите [MS Visual C](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist).

Запустите Powershell, набрав комбинацию клавиш Win+X и выбрав запуск от обычного пользователя.

### Установка и запуск

Установите проект со всеми зависимостями:
```shell
python3 -m pip install sevimon
```

В процессе могут выводиться предупреждения с просьбой добавить путь к исполняемым файлам в переменные среды -- это следует сделать.

Для старта основной программы используйте команду `sevimon`. При первом запуске скачиваются модели, создаётся текстовый конфигурационный файл.
Для настройки можно запустить программу `sevicfg`.
Для отображения статистики используйте команду `sevistat`. Перед этим её должно быть накоплено хотя бы 2 часа.

## Лицензия файлов проекта

AGPL v3 или более новая.

## Благодарности

Для поиска лиц на изображении используются наработки проекта [Centerface](https://github.com/Star-Clouds/CenterFace/blob/master/prj-python/).
Для определения эмоций используется проект [HSEmotion](https://github.com/HSE-asavchenko/face-emotion-recognition).
