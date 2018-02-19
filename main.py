import sys

from ic import *
from decrypt import *

total = 0
file = open(sys.argv[1], 'r')
ic = ioc(file)
freqs = findnfreqs(file, 1)

# print(sorted(freqs.items()))
nicef = [(v, k) for k, v in freqs.items()]
nicef.sort(reverse=True)
# for keys, values in nicef:
#     print(keys, values)

shift_key, shift_ptx = shift(nicef, file)
vig_key, vig_ptx = vigenere(file, ic)

print("Which cipher appears to be correct?")

print("Shift cipher")
print("Key:", shift_key)
print("Plaintext:")
print(shift_ptx, "\n\n")

print("Vigenere cipher")
print("Key:", vig_key)
print("Plaintext:")
print(vig_ptx, "\n\n")

# CIPHER 1: SHIFT CIPHER (R TO E)
# CIPHER 2: ? (IOC HIGHER to 0.07)
# CIPHER 3: VIGENERE (KEY IS STBRNM)
# CIPHER 4: