# Licensed under AGPLv3+

import configparser
import platformdirs
import os

from lib.i18n import _


ANAME = "sevimon"
emotions = (_("Anger "), _("Contm."), _("Disgu."), _("Fear  "), _("Happs."), _("Neutr."), _("Sadns."), _("Surpr."))


class configclass:
    def __init__(self,):
        pass

# Simple sanity check for input string
# Args: input string, default array
def get_check_ints(sec, name, defv):
    try:
        s = sec.get(name)

        if not set(s).issubset(set(" \t,0123456789")):
            return defv

        res = [int(ele) for ele in s.split(',')]

        if (len(res) != len(defv)):
            return defv
    except Exception as exc:
        return defv

    return res


def get_check_floats(sec, name, defv):
    try:
        s = sec.get(name)

        if not set(s).issubset(set(" \t.,0123456789")):
            return defv

        res = [float(ele) for ele in s.split(',')]

        if (len(res) != len(defv)):
            return defv
    except Exception as exc:
        return defv

    return res


def get_check_bools(sec, name, defv):
    try:
        s = sec.get(name)

        if not set(s).issubset(set(" \t,TrueFalse")):
            return defv

        s = s.replace(' ', '').replace('\t', '')
        tmps = [ele for ele in s.split(',')]

        res = []
        for i in tmps:
            if i == "True":
                res.append(True)
            elif i == "False":
                res.append(False)
            else:
                return defv

        if (len(res) != len(defv)):
            return defv
    except Exception as exc:
        return defv

    return res


def readcfg() -> configclass:
    cfg = configclass()

    config = configparser.ConfigParser()
    configname = platformdirs.user_config_dir(ANAME) + "/" + ANAME + ".cfg"
    print(_("Trying to read the config file ") + configname)
    try:
        config.read(configname)
    except Exception as exc:
        pass

    try:
        section = config["common"]
    except:
        config.add_section("common")
        section = config["common"]
        pass

    cfg.camera_dev = get_check_ints(section,"camera_dev", [0])[0]
    cfg.res = get_check_ints(section,"res", [640, 480])
    cfg.fps = get_check_floats(section,"fps", [1.0])[0]
    cfg.wdelay = get_check_ints(section,"wdelay", [0])[0]

    cfg.showcap = get_check_bools(section,"showcap", [True])[0]
    cfg.allfaces = get_check_bools(section,"allfaces", [False])[0]

    cfg.writestat = get_check_bools(section,"writestat", [True])[0]

    cfg.wsize = get_check_ints(section,"wsize", [95])[0]
    cfg.wpos = get_check_ints(section,"wpos", [300, 150])
    cfg.wcolor = tuple(get_check_ints(section,"wcolor", [0, 255, 0]))

    cfg.showwarn = get_check_bools(section,"showwarn", [True])[0]
    cfg.beepwarn = get_check_bools(section,"beepwarn", [False])[0]

    cfg.wmax = get_check_floats(section,"wmax",
            [4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5])
    cfg.wmin = get_check_floats(section,"wmin",
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    cfg.wmaxen = get_check_bools(section,"wmaxen",
            [True, False, False, False, False, False, False, True])
    cfg.wminen = get_check_bools(section,"wminen",
            [False, False, False, False, False, False, False, False])

    return cfg


def writecfg(cfg) -> None:
    config = configparser.ConfigParser()
    configname = platformdirs.user_config_dir(ANAME) + "/" + ANAME + ".cfg"
    os.makedirs(platformdirs.user_config_dir(ANAME), exist_ok=True)

    with open(configname, 'w') as configfile:
        config.add_section("common")
        section = config["common"]
        section["camera_dev"] = str(cfg.camera_dev)
        section["res"] = str(cfg.res).replace('[', '').replace(']', '')
        section["fps"] = str(cfg.fps)
        section["wdelay"] = str(cfg.wdelay)
        section["showcap"] = str(cfg.showcap)
        section["allfaces"] = str(cfg.allfaces)
        section["writestat"] = str(cfg.writestat)
        section["wsize"] = str(cfg.wsize)
        section["wpos"] = str(cfg.wpos).replace('[', '').replace(']', '')
        section["wcolor"] = str(cfg.wcolor).replace('(', '').replace(')', '')
        section["showwarn"] = str(cfg.showwarn)
        section["beepwarn"] = str(cfg.beepwarn)
        section["wmax"] = str(cfg.wmax).replace('[', '').replace(']', '')
        section["wmin"] = str(cfg.wmin).replace('[', '').replace(']', '')
        section["wmaxen"] = str(cfg.wmaxen).replace('[', '').replace(']', '')
        section["wminen"] = str(cfg.wminen).replace('[', '').replace(']', '')

        if not os.path.exists(platformdirs.user_config_dir(ANAME)):
            os.makedirs(platformdirs.user_config_dir(ANAME))
        print(_("Writing to the config file ") + configname)
        config.write(configfile)

# vi: tabstop=4 shiftwidth=4 expandtab
