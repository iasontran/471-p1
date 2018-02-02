#!/usr/bin/python

from freq import *

def ioc(len):
    #file = open(sys.argv[1], 'r')
    #ct = file.read()
    ct = len
    icsum = 0.0

    n = len(ct)
    freqs = findnfreqs(ct, 1)
    for x in freqs.values():
        icsum += x * ((x * n - 1)/(n - 1))

    return icsum