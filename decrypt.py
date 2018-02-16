import sys
from ic import *
from operator import itemgetter
import string
from collections import Counter


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


def vigenere(freqs, file, ioc):
    """Consider cipher is polyalphabetic """
    ctx = file.read()
    file.seek(0, 0)

    ic_eng = 0.066895

    periods = period_attempt(ctx, ic_eng, ioc)
    init_period = periods[0][0]
    key, ptx = vigenere_decrypt(ctx, ic_eng, init_period)

    return key, ptx


def vigenere_decrypt(ctx, ic_eng, period):
    """Decryption/cracking process for Vigenere ciphertext"""

    return key, ptx


def period_attempt(ctx, ic_eng, ic_ctx):
    """Attempt to guess periods in ciphertext"""
    kas = kasiski(ctx)
    kas.sort()

    """If kasiski method did not work, exit"""
    if not kas:
        return

    periods = [period for period,  in kas]
    ics = compute_periods_with_ic(ctx, ic_eng, ic_ctx)
    ics.sort()

    guess_per = [(period, kas[i][1] + ics[i][1]) for i,period in enumerate(periods)]

    guess_per.sort(key = itemgetter(1), reverse = True)
    prob_tot = sum([prob for _,prob in guess_per])
    guess_per = [(period, "{0:.2f}%".format(100 * prob/prob_tot)) for period, prob in guess_per]

    return guess_per


def find_trigram(ctx):
    """Find trigrams within the ciphertext"""
    tri = {}

    for i in range(len(ctx) - 3 + 1):
        curr_gram = ctx[i:i + 3]
        tri[curr_gram] = tri.get(curr_gram, 0) + 1

    tri = sorted(tri.items(), key=itemgetter(1), reverse=True)
    tri = [(a_gram, occur) for a_gram, occur in tri if occur > 1]

    return tri


def kasiski(ctx):
    """Periods found utilizing the Kasiski Method"""
    ngram = find_trigram(ctx)

    """Fail method if no trigrams are found"""
    if not ngram:
        return

    kas = []
    for ngram, occur in ngram:
        next_pos = 0
        for i in range(occur - 1):
            curr_pos = ctx.find(ngram, next_pos)
            next_pos = ctx.find(ngram, next_pos + 1)
            dist = next_pos - curr_pos

            for period in range(2, dist + 1):
                if dist % period == 0:
                    kas.append(period)

    kas = Counter(kas).most_common(5)
    occur_tot = sum([occurrences for _, occurrences in kas])
    kas = [(period, occurrences/occur_tot) for period, occurrences in kas]

    return kas


def average_ic(ctx, per):
    """Calculate average of IOC of the period subsequences"""
    subseq = [[] for i in range(per)]

    for position, letter in enumerate(ctx):
        subseq[position % letter].append(letter)

    subseq = [''.join(subsequence) for subsequence in subseq]
    average = sum([ioc(subsequence) for subsequence in subseq])/per

    return float("{0:.6f}".format(average))


def compute_periods_with_ic(ctx, ic_eng, ic_ctx, periods=None):
    """Compute periods given index of coincidence values"""

    if periods is None:
        periods = range(1, 21)

    ic_averages = []

    for period in periods:
        averages = average_ic(ctx, period)
        ic_averages.append((period, averages))

    """Difference of index of coincidence with regards to the english language"""
    diff_eng_ic = [(period, abs(average_ioc - ic_eng)) for period, average_ioc in ic_averages]
    """Total difference for the english language"""
    diff_tot_eng = sum([1/diff for period, diff in diff_eng_ic])

    per_1 = [(period, (1/diff)/diff_tot_eng) for period, diff in diff_eng_ic]
    """Index of coincidence values across all periods"""
    periods_ic = [(period, expected_ic(ctx, period, ic_eng)) for period in periods]
    """Difference between period IOC values and ciphertext IOC values"""
    diff_ctx_ic = [(period, abs(period_ic - ic_ctx)) for period, period_ic in periods_ic]
    """Total difference with regards to the ciphertext"""
    diff_tot_ctx = sum([1/difference for period, difference in diff_ctx_ic])

    per_2 = [(period, 1/difference/diff_tot_ctx) for period, difference in diff_ctx_ic]
    """Periods with probabilities"""
    prob_period = [(period, per_1[i][1] + per_2[i][1]) for i, period in enumerate(periods)]

    prob_period.sort(key=itemgetter(1), reverse=True)

    prob_tot = sum([prob for _, prob in prob_period])

    prob_period = [(period, prob/prob_tot) for period, prob in prob_period]

    return prob_period


def expected_ic(ctx, per, ic_eng):
    """Calculates the expected index of coincidence given a specified period"""
    return 1/per * (per - len(ctx))/(len(ctx) - 1) * ic_eng + (per - 1)/per * len(ctx)/(len(ctx) - 1) * 1/26


#
# def sub():
#
#     return sub
#
#
# def pad():
#
#     return pad
#
#
# def perm():
#
#     return perm

