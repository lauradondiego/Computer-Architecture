#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
print("sysargv", sys.argv)
cpu.load(sys.argv[1])
cpu.run()
