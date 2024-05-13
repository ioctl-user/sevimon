# Licensed under AGPLv3+

import configparser
import platformdirs
import ast
import os

from lib.i18n import _


ANAME = "sevimon"
emotions = (_("Anger "), _("Contm."), _("Disgu."), _("Fear  "), _("Happs."), _("Neutr."), _("Sadns."), _("Surpr."))


class configclass:
    def __init__(self,):
        pass


def readcfg() -> configclass:
    cfg = configclass()

    config = configparser.ConfigParser()
    configname = platformdirs.user_config_dir(ANAME) + "/" + ANAME + ".cfg"
    print(_("Trying to read the config file ") + configname)
    config.read(configname)

    needwritecfg = "common" not in config
    if needwritecfg:
        config.add_section("common")
    section = config["common"]

    cfg.camera_dev = section.getint("camera_dev", 0)
    cfg.res = ast.literal_eval(section.get("res", "[640, 480]"))
    cfg.fps = section.getfloat("fps", 1)
    cfg.wdelay = section.getint("wdelay", 0)

    cfg.showcap = section.getboolean("showcap", True)
    cfg.allfaces = section.getboolean("allfaces", False)

    cfg.writestat = section.getboolean("writestat", True)

    cfg.wsize = section.getint("wsize", 95)
    cfg.wpos = ast.literal_eval(section.get("wpos", "[300, 150]"))
    cfg.wcolor = ast.literal_eval(section.get("wcolor", "(0, 255, 0)"))

    cfg.showwarn = section.getboolean("showwarn", True)
    cfg.beepwarn = section.getboolean("beepwarn", False)

    cfg.wmax = ast.literal_eval(section.get(
            "wmax", "[4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5]"))
    cfg.wmin = ast.literal_eval(section.get(
            "wmin", "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"))

    cfg.wmaxen = ast.literal_eval(section.get(
            "wmaxen", "[True, False, False, False, False, False, False, True]"))
    cfg.wminen = ast.literal_eval(section.get(
            "wminen", "[False, False, False, False, False, False, False, False]"))

    if needwritecfg:
        writecfg(cfg)

    return cfg


def writecfg(cfg) -> None:
    config = configparser.ConfigParser()
    configname = platformdirs.user_config_dir(ANAME) + "/" + ANAME + ".cfg"
    os.makedirs(platformdirs.user_config_dir(ANAME), exist_ok=True)

    with open(configname, 'w') as configfile:
        config.add_section("common")
        section = config["common"]
        section["camera_dev"] = str(cfg.camera_dev)
        section["res"] = str(cfg.res)
        section["fps"] = str(cfg.fps)
        section["wdelay"] = str(cfg.wdelay)
        section["showcap"] = str(cfg.showcap)
        section["allfaces"] = str(cfg.allfaces)
        section["writestat"] = str(cfg.writestat)
        section["wsize"] = str(cfg.wsize)
        section["wpos"] = str(cfg.wpos)
        section["wcolor"] = str(cfg.wcolor)
        section["showwarn"] = str(cfg.showwarn)
        section["beepwarn"] = str(cfg.beepwarn)
        section["wmax"] = str(cfg.wmax)
        section["wmin"] = str(cfg.wmin)
        section["wmaxen"] = str(cfg.wmaxen)
        section["wminen"] = str(cfg.wminen)

        if not os.path.exists(platformdirs.user_config_dir(ANAME)):
            os.makedirs(platformdirs.user_config_dir(ANAME))
        print(_("Writing to the config file ") + configname)
        config.write(configfile)

# vi: tabstop=4 shiftwidth=4 expandtab
