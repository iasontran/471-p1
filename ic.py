#!/usr/bin/python

import sys
from freq import *


def ic(freq):
    file = open(sys.argv[1], 'r')
    ct = file.read()
    icsum = 0.0

    n = len(ct)

    for x in freq.values():
        icsum += x * (n - 1)

    index = icsum / (n * (n - 1))
    return index