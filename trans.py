import math
import decrypt



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
        