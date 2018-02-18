import operator

def decryptshift(string,shift):
    string=string.upper()#make sure it is all uppercase
    string=string.strip()
    string=string.replace(" ","")
    decrypt=""
    for letter in string:
        x=ord(letter)#ascii for the letter
        if x+shift > 90:
            decrypt+=(chr(shift-(90-x)+65-1))#handles edge cases so it loops back to beginning of alphabet
        else:
            decrypt+=(chr(x+shift))
            
    return decrypt
#note to get shift amount just find most freq letter and assume it is e and subtract the difference between the letters
#inputs the dictionary of frequencies 
#outputs the shift amount
def getshift(dict_freq):
    shifted=max(dict_freq.iteritems(), key=operator.itemgetter(1))[0]
    
    shifted=ord(shifted)
    
    shift=shifted-ord('E')
    
    if shift < 0:
        shift+=26
        
    return shift