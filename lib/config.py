import configparser
import platformdirs
import ast
import os

APPNAME = "sevimon"

class configclass:
     def __init__(self,):
        pass

def readcfg() -> configclass:
    cfg = configclass()

    config = configparser.ConfigParser()
    configname = platformdirs.user_config_dir(APPNAME) + "/" + APPNAME + ".cfg"
    print("Trying to read the config file " + configname)
    config.read(configname)

    needwritecfg = "common" not in config
    if needwritecfg:
        config.add_section("common")
    section = config["common"]

    cfg.camera_dev = section.getint("camera_dev", 0)
    cfg.img_w = section.getint("img_w", 640)
    cfg.img_h = section.getint("img_h", 480)
    cfg.fps = section.getint("fps", 1)

    cfg.showcap = section.getboolean("showcap", True)

    cfg.writestat = section.getboolean("writestat", True)

    cfg.wsize = section.getint("wsize", 95)
    cfg.wx = section.getint("wx", 300)
    cfg.wy = section.getint("wy", 150)
    cfg.wcolor = ast.literal_eval(section.get("wcolor", "(0, 255, 0)"))

    cfg.showwarn = section.getboolean("showwarn", True)

    cfg.wmax = ast.literal_eval(section.get("wmax", "[ 4.0, None, None, None, None, None, None,  1.5]"))
    cfg.wmin = ast.literal_eval(section.get("wmin", "[None, None, None, None, None, None, None, None]"))

    if needwritecfg:
        writecfg(cfg)

    return cfg

def writecfg(cfg) -> None:
    config = configparser.ConfigParser()
    configname = platformdirs.user_config_dir(APPNAME) + "/" + APPNAME + ".cfg"

    with open(platformdirs.user_config_dir(APPNAME) + "/" + APPNAME + ".cfg", 'w') as configfile:
        config.add_section("common")
        section = config["common"]
        section["camera_dev"] = str(cfg.camera_dev)
        section["img_w"] = str(cfg.img_w)
        section["img_h"] = str(cfg.img_h)
        section["fps"] = str(cfg.fps)
        section["showcap"] = str(cfg.showcap)
        section["writestat"] = str(cfg.writestat)
        section["wsize"] = str(cfg.wsize)
        section["wx"] = str(cfg.wx)
        section["wy"] = str(cfg.wy)
        section["wcolor"] = str(cfg.wcolor)
        section["showwarn"] = str(cfg.showwarn)
        section["wmax"] = str(cfg.wmax)
        section["wmin"] = str(cfg.wmin)

        if not os.path.exists(platformdirs.user_config_dir(APPNAME)):
            os.makedirs(platformdirs.user_config_dir(APPNAME))
        print("Writing to the config file " + configname)
        config.write(configfile)
