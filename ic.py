#!/usr/bin/python

from freq import *
from collections import Counter


def ioc(file):
    # file = open(sys.argv[1], 'r')
    # ct = file.read()
    icsum = 0.0
    ct = file.read()
    file.seek(0, 0)

    n = len(ct)
    freqs = findnfreqs(file, 1)

    for x in freqs.values():
        icsum += x * ((x * n - 1)/(n - 1))

    # for x in freqs.values():
    #     icsum += (x * (x - 1))/(n * (n - 1))

    return icsum


def ioc_subseq(subseq):
    """Find the IOC of a subsequence of text (for Vigenere cipher)"""
    ioc_sum = 0
    n = len(subseq)

    for x in Counter(subseq).values():
        ioc_sum += (x * (x - 1))/(n * (n - 1))

    return ioc_sum
