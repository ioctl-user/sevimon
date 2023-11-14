#!/usr/bin/python3

# Licensed under AGPLv3

from matplotlib import pyplot as plt
import os
import sys
import configparser
import platformdirs

sys.path.append(os.path.dirname(__file__))
from lib.i18n import _
from lib.config import *


def main() -> None:

    x = []
    dtime = []
    ang = []
    cont = []
    disq = []
    fear = []
    happ = []
    neutr = []
    sad = []
    surp = []

    #cutlen = 16 # Hack to ignore seconds
    cutlen = 13 # Hack to ignore minutes

    # Read all files in the log dir
    dtold = None
    i = 0
    curx = 0
    logdir = platformdirs.user_log_dir(ANAME)
    print(_("Scanning directory {} for statistics").format(logdir))
    for logname in sorted(os.listdir(logdir)):
        date = logname
        year, mon, day = logname.split(".")

        with open(logdir + "/" + logname, 'r') as f:
            for record in f:
                hms, _ang, _cont, _disq, _fear, _happ, _neutr, _sad, _surp = record.split()
                hour, mn, sec = hms.split(":")
                dt = date + " " + hms
                dt = dt[:cutlen]
                if dt == dtold:
                    m_ang += float(_ang)
                    m_cont += float(_cont)
                    m_disq += float(_disq)
                    m_fear += float(_fear)
                    m_happ += float(_happ)
                    m_neutr += float(_neutr)
                    m_sad += float(_sad)
                    m_surp += float(_surp)
                    i = i + 1
                    continue
                else:
                    if not dtold == None:
                        dtime.append('{:02}-{:02} {:02}:{:02}'.format(o_mon, o_day, o_hour, o_mn))
                        ang.append(m_ang / i)
                        cont.append(m_cont / i)
                        disq.append(m_disq / i)
                        fear.append(m_fear / i)
                        happ.append(m_happ / i)
                        neutr.append(m_neutr / i)
                        sad.append(m_sad / i)
                        surp.append(m_surp / i)
                        x.append(curx)
                        curx += 1
                    o_year = int(year)
                    o_mon = int(mon)
                    o_day = int(day)
                    o_hour = int(hour)
                    o_mn = int(mn)
                    o_sec = int(sec)

                    m_ang = 0.0
                    m_cont = 0.0
                    m_disq = 0.0
                    m_fear = 0.0
                    m_happ = 0.0
                    m_neutr = 0.0
                    m_sad = 0.0
                    m_surp = 0.0

                    dtold = dt
                    i = 0

    # Finilize last interval
    if not i == 0:
        dtime.append('{:02}-{:02} {:02}:{:02}'.format(o_mon, o_day, o_hour, o_mn))
        ang.append(m_ang / i)
        cont.append(m_cont / i)
        disq.append(m_disq / i)
        fear.append(m_fear / i)
        happ.append(m_happ / i)
        neutr.append(m_neutr / i)
        sad.append(m_sad / i)
        surp.append(m_surp / i)
        x.append(curx)

    plt.plot(ang, color="red", label=emotions[0], markersize=1, linestyle='-')
    plt.plot(cont, color="green", label=emotions[1], markersize=1, linestyle='-')
    plt.plot(disq, color="blueviolet", label=emotions[2], markersize=1, linestyle='-')
    plt.plot(fear, color="brown", label=emotions[3], markersize=1, linestyle='-')
    plt.plot(happ, color="orange", label=emotions[4], markersize=1, linestyle='-')
    plt.plot(neutr, color="gray", label=emotions[5], markersize=1, linestyle='-')
    plt.plot(sad, color="black", label=emotions[6], markersize=1, linestyle='-')
    plt.plot(surp, color="royalblue", label=emotions[7], markersize=1, linestyle='-')

    plt.xticks(x, dtime,  rotation=80)

    plt.margins(x=0.0, y=0.0)
    plt.legend()
    plt.subplots_adjust(bottom=0.2, top=0.98, left=0.03, right=0.97)
    plt.show()


if __name__ == "__main__":
    main()

# vi: tabstop=4 shiftwidth=4 expandtab
