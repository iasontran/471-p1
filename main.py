import sys

from ic import *
from decrypt import *

total = 0
file = open(sys.argv[1], 'r')
ic = ioc(file)
freqs = findnfreqs(file, 1)

# print(sorted(freqs.items()))
# nicef = [ (v, k) for k, v in freqs.items()]
# nicef.sort(reverse=True)
# for keys, values in nicef:
#     print(keys, values)
# print(ic)
# shift_ctx = shift(nicef, file)
# print(shift_ctx)

key, ptx = vigenere(file, ic)

print(key)
print(ptx)

# CIPHER 1: SHIFT CIPHER (R TO E)
# CIPHER 2: ? (IOC HIGHER to 0.07)
# CIPHER 3: VIGENERE (IOC LOWER TO 0.041)
# CIPHER 4: ONE-TIME PAD?