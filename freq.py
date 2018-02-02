import sys

import io

def findnfreqs(lines,n):
    lx={}
    total=0
    #for lines in f:
    for i in range(0,len(lines),1):
        #print(lines[i:i+n])
        if(len(lines[i:i+n]) == n):
            try:
                lx[lines[i:i+n]]+=1
                total+=1
            except:
                lx[lines[i:i+n]]=1
                total+=1
    for y in lx.keys():
        lx[y]=lx[y]/total
    #f.seek(0,0)
    return lx
#cfile=sys.argv[1]
#with open(cfile,'r') as f:
#    x=findnfreqs(f,1)
#    print(x)
#    yx=findnfreqs(f, 2)
#    print(yx)

        

