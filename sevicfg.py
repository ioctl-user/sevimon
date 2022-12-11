#!/usr/bin/python3

# Licensed under AGPLv3+

import sys
import os

sys.path.append(os.path.dirname(__file__))
from lib.guicfg import *


def main() -> None:
    cfg = readcfg()
    guiconfigurator(cfg)

if __name__ == "__main__":
    main()

# vi: tabstop=4 shiftwidth=4 expandtab
