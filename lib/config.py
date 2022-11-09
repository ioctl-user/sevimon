import configparser
import platformdirs
import ast
import os

APPNAME = "sevimon"

config = configparser.ConfigParser()
config.read(platformdirs.user_config_dir(APPNAME) + '/sevimon.cfg')
try:
    cfg = config["common"]
    writecfg = False
except:
    config.add_section("common")
    cfg = config["common"]
    writecfg = True


CAMERA_DEV = cfg.getint("camera_dev", 0)
IMG_W = cfg.getint("img_w", 640)
IMG_H = cfg.getint("img_h", 480)
FPS = cfg.getint("fps", 1)

SHOWCAP = cfg.getboolean("showcap", True)

WRITESTAT = cfg.getboolean("writestat", True)

WSIZE = cfg.getint("wsize", 95)
WX = cfg.getint("wx", 300)
WY = cfg.getint("wy", 150)
WCOLOR = ast.literal_eval(cfg.get("wcolor", "(0, 255, 0)"))

SHOWWARN = cfg.getboolean("showwarn", True)

WMAX = ast.literal_eval(cfg.get("wmax", "[ 4.0, None, None, None, None, None, None,  1.5]"))
WMIN = ast.literal_eval(cfg.get("wmin", "[None, None, None, None, None, None, None, None]"))

if writecfg:
    if not os.path.exists(platformdirs.user_config_dir(APPNAME)):
        os.makedirs(platformdirs.user_config_dir(APPNAME))
    with open(platformdirs.user_config_dir(APPNAME) + '/sevimon.cfg', 'w') as configfile:
        config.set("common", "camera_dev", str(CAMERA_DEV))
        config.set("common", "img_w", str(IMG_W))
        config.set("common", "img_h", str(IMG_H))
        config.set("common", "fps", str(FPS))
        config.set("common", "showcap", str(SHOWCAP))
        config.set("common", "writestat", str(WRITESTAT))
        config.set("common", "wsize", str(WSIZE))
        config.set("common", "wx", str(WX))
        config.set("common", "wy", str(WY))
        config.set("common", "wcolor", str(WCOLOR))
        config.set("common", "showwarn", str(SHOWWARN))
        config.set("common", "wmax", str(WMAX))
        config.set("common", "wmin", str(WMIN))

        config.write(configfile)
