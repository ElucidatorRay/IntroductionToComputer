import time
import sys

k = int(sys.argv[1])
N = int(sys.argv[2])
m = int(sys.argv[3])

def DegreeRemainder(k,N,m):
    '''A function to calculate the remainder of k^N divided by m'''
    #Set the base with k%m and later degree start from 1
    base = k%m
    i = 1
    #the list save each remainder of the k^index
    L = [base]
    #use former term to calculate the current term
    while(2**i < N):
        L.append( (L[i-1]*L[i-1])%m )
        i+=1
    #the last index has over N,delete it. then assign the value to top for the later loop
    i = i-1
    top = i
    L2 = []
    #build a new list to save 0 or 1 which is the binary representation of N
    for i in range(top+1):
        L2.append(0)
    #from the most large term. if larger then minus it 
    for i in range(top,-1,-1):
        if 2**i <= N:
            L2[i] = 1
            N = N - 2**i
        elif N == 0:
            break
    Ans = 1
    #if data in L2 is 1, combine each remainder
    for i in range(0,top + 1):
        if L2[i] > 0:
            Ans = ( ( (Ans)*L[i] )%m )
    print(Ans)
        
start = time.time()
DegreeRemainder(k,N,m)
end = time.time()
print('time:',(end - start),'s')