from freq import *
from ic import *
from shift import *
from trans import *
from decrypt import *


ic_eng = 0.066895
total = 0
file = open(sys.argv[1], 'r')

ic = ioc(file)
freqs = findnfreqs(file, 1)
#freqs2 = findnfreqs(file, 2)

#print(sorted(freqs.items()))
print("Displaying frequencies of ciphertext:")
nicef = [(v, k) for k, v in freqs.items()]
nicef.sort(reverse=True)
for keys, values in nicef:
    print(keys, values)
print("Displaying index of coincidence:")
print(ic)

maxkey = max(freqs.items(), key=operator.itemgetter(1))[0]
minkey = min(freqs.items(), key=operator.itemgetter(1))[0]

if freqs[maxkey]-freqs[minkey] < .05:
    print("This is a one-time pad cipher since the letter frequencies are so similar.")
    print("Can not decrypt ending progrm")
    sys.exit()
elif abs(ic_eng - ic) > .005:
    print("This is a vigenere cipher since the letter frequencies are not as spread out as the english language, and the index of coincidence is not similair to the english language.")
    vig_key, vig_ptx = vigenere(file, ic)
    print("Plaintext: ", vig_ptx)
    print("Key: ", vig_key)
else:
    print("This is a substitution cipher, since our preliminary analysis of the ciphertexts shows there were no permutation ciphers")
    print("Also since substitution ciphers can be done manually assuming this is a shift cipher")
    #implement shift decrpyt here
    shift=getshift(freqs)
    decrypt=decryptshift(file, shift)
    print(decrypt)
    print("shift amount was", shift)
    p=input("Confirm if this is the plaintext, if not then this was a substitution cipher done manually. Press Q to quit")
    if p.strip().upper().startswith('Q'):
            sys.exit()
def transp():
    data=file.read().replace('\n','')
    file.seek(0,0)
    
    print(data)
    
    transtry=iterkeys(data)
    if data == None:
        print("Decryption failed")
    else:
        print("Decrypted text")
        print(transtry)