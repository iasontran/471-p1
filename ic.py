#!/usr/bin/python

import sys


def ic():
    file = open(sys.argv[1], 'r')
    ct = file.read()
    freq = {}
    icsum = 0.0

    n = len(ct)

    for x in freq.values():
        icsum += x * (n - 1)

    index = icsum / (n * (n - 1))
    return index