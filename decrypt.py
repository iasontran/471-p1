import sys


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shift(freqs, file):
    ctx = file.read()
    file.seek(0, 0)
    key = guess_key(freqs)

    ptx = ""
    for letter in ctx:
        index = alphabet.find(letter)
        new_index = flat(index - key)
        ptx += alphabet[new_index]

    return ptx

def guess_key(freqs):
    most_common = 4  # letter E
    second_item = [seq[1] for seq in freqs]
    key = alphabet.find(second_item[0]) - most_common
    return key

def flat(num):
    return num - (26 * (num // 26))

# def kasiski():
#
#     return kas
#
# def vignere():
#
#     return vig
#
# def sub():
#
#     return sub
#
# def pad():
#
#     return pad
#
# def perm():
#
#     return perm