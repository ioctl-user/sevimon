#!/usr/bin/python3

# Licensed under AGPLv3+

import sys
import os

sys.path.append(os.path.dirname(__file__))
from lib.guicfg import *


if __name__ == "__main__":
    cfg = readcfg()
    guiconfigurator(cfg)

# vi: tabstop=4 shiftwidth=4 expandtab
