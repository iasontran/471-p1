from ic import *
from operator import itemgetter
from collections import Counter
from itertools import zip_longest

import math

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
top_five_common = "ETAOI"
ic_eng = 0.066895


"""Shift cipher related functions"""


def shift(freqs, file):
    ctx = file.read()
    file.seek(0, 0)
    key = guess_key(freqs)

    ptx = ""
    for letter in ctx:
        index = alphabet.find(letter)
        new_index = flat(index - key)
        ptx += alphabet[new_index]

    return key, ptx


def guess_key(freqs):
    most_common = 4  # letter E
    second_item = [seq[1] for seq in freqs]
    key = alphabet.find(second_item[0]) - most_common
    return key


def flat(num):
    return num - (26 * (num // 26))


"""Vigenere cipher related functions"""


def vigenere(file, index_of_coincidence):
    """Consider cipher is polyalphabetic """
    ctx = file.read()
    file.seek(0, 0)

    periods = period_attempt(ctx, index_of_coincidence)
    init_period = periods[0][0]
    key, ptx = vigenere_decrypt(ctx, init_period)

    return key, ptx


def vigenere_decrypt(ctx, period):
    """Decryption/cracking process for Vigenere ciphertext"""
    subseq = [[] for i in range(period)]
    for position, letter in enumerate(ctx):
        subseq[position % period].append(letter)

    subseq = [''.join(subsequence) for subsequence in subseq]
    key = ""
    subseq_dec = ['' for _ in subseq]

    for i_sub, subsequence in enumerate(subseq):

        most_common_ctx = Counter(subsequence).most_common(5)
        most_common_ctx.sort(key=itemgetter(1, 0), reverse=True)

        most_common_ptx = top_five_common[0]
        most_common_ptx_enc_cnt = []

        for i_letter, letter in enumerate(most_common_ctx):

            most_common_ptx_enc = most_common_ctx[i_letter][0]

            offset = (alphabet.index(most_common_ptx_enc) - alphabet.index(most_common_ptx)) % 26

            matching = 0

            for letter_ctx in most_common_ctx:

                alpha_pos = alphabet.index(letter_ctx[0])
                letter_dec = alphabet[(alpha_pos - offset) % 26]

                if letter_dec in top_five_common:
                    matching += 1
                    most_common_ptx_enc_cnt.append((most_common_ptx_enc, matching))

        """"""
        most_common_ptx_enc_cnt.sort(key=itemgetter(1), reverse=True)
        matching_tot = sum([matching for _, matching in most_common_ptx_enc_cnt])
        most_common_ptx_enc_cnt = [(letter, "{0:.2f}%".format(100 * match/matching_tot))
                                   for letter, match in most_common_ptx_enc_cnt]

        most_common_ptx_enc = most_common_ptx_enc_cnt[0][0]

        offset = alphabet.index(most_common_ptx_enc) - alphabet.index(most_common_ptx) % 26

        letter_key = alphabet[offset - 1]
        key += letter_key

        subsequence_dec = subsequence

        for position, letter in enumerate(alphabet):
            subsequence_dec = subsequence_dec.replace(letter, alphabet[(position - offset) % 26].lower())

        subseq_dec[i_sub] = subsequence_dec

    subseq_dec_mix = zip_longest(*subseq_dec, fillvalue='')
    subseq_dec_mix = [''.join(subsequence_mix) for subsequence_mix in subseq_dec_mix]

    ptx = ''.join(subseq_dec_mix)
    ptx = rejoin(ptx, ctx)

    return key, ptx.upper()


def rejoin(ptx, ctx):

    rejoined = list(ptx)
    for position, letter in enumerate(ctx.upper()):
        if letter not in alphabet:
            rejoin(position, letter)

    return ''.join(rejoined)


def period_attempt(ctx, ic_ctx):
    """Attempt to guess periods in ciphertext"""
    kas = kasiski(ctx)
    kas.sort()

    """If kasiski method did not work, exit"""
    if not kas:
        return

    periods = [period for period, _ in kas]
    ics = compute_periods_with_ic(ctx, ic_ctx, periods)
    ics.sort()

    guess_per = [(period, kas[i][1] + ics[i][1]) for i, period in enumerate(periods)]

    guess_per.sort(key=itemgetter(1), reverse=True)
    prob_tot = sum([prob for _, prob in guess_per])
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
    for n_gram, occur in ngram:
        next_pos = 0
        for i in range(occur - 1):
            curr_pos = ctx.find(n_gram, next_pos)
            next_pos = ctx.find(n_gram, curr_pos + 1)
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
        subseq[position % per].append(letter)

    subseq = [''.join(subsequence) for subsequence in subseq]
    average = sum([ioc_subseq(subsequence) for subsequence in subseq])/per

    return float("{0:.6f}".format(average))


def compute_periods_with_ic(ctx, ic_ctx, periods=None):
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
    periods_ic = [(period, expected_ic(ctx, period)) for period in periods]
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


def expected_ic(ctx, per):
    """Calculates the expected index of coincidence given a specified period"""
    return 1 / per * (len(ctx) - per) / (len(ctx) - 1) * ic_eng + (per - 1) / per * len(ctx) / (len(ctx) - 1) * 1 / 26


"""Substitution cipher related functions done manually"""


"""One-time pad related functions none since can't decrpyt"""




"""Permutation cipher related functions"""


def decrypttrans(key,string):
    cols=math.ceil(len(string)/key)#the number of cols in transposition
    
    rows=key#number of rows in transposition
    
    emptyspace= (cols*rows) - len(string)
    
    plaintext= ['']*cols
    
    #pointing to next char in transposition grid
    col=0
    row=0
    for col in range(0,cols):
        plaintext= ['']*cols
        for chars in string:
            plaintext[col]+= chars
            #go to next col
            col+=1
            #if no more cols reset and go to next row
            #or at an empty space (place in grid with no cipher text)
            if (col == cols) or (col == cols -1 and row >= rows-emptyspace):
                col=0 #reset col
                row+=1 #increase the row
            
        print('Trying key',key)
        xp=''.join(plaintext)
        print(xp)
        print("Enter Q if this is plaintext otherwise press anything else")
        x=input("--")
        if x.strip().upper().startswith('Q'):
            return ''.join(plaintext)     
    return ''.join(plaintext)


def iterkeys(string):
    
    for key in range(1,len(string)):
        print('Trying key #',key)
        
        decrypt=decrypttrans(key, string)
        print(decrypt)
        print("Enter Q if this is plaintext otherwise press anything else")
        x=input("--")
        if x.strip().upper().startswith('Q'):
            return decrypt
    return None
def transp(file):
    data=file.read().replace('\n','')
    file.seek(0,0)
    
    print(data)
    
    transtry=iterkeys(data)
    if data == None:
        print("Decryption failed")
    else:
        print("Decrypted text")
        print(transtry)
