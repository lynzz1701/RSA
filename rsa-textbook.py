import random

def MillerRabin(n, times):
    m = n - 1
    k = 0
    while m % 2 == 0:
        m = m // 2  
        k += 1
    for i in range(0, times):
        isPrime = False
        a = random.randint(1, n - 1)
        b = pow(a, m, n)
        b = b % n
        if b == 1:
            isPrime = True
        for j in range(0, k):
            if b == n - 1:
                isPrime = True
                break
            b = (b * b) % n
        if not isPrime:
            return False
    return True


def PQGenerate(len):
    isPrime = False
    while(not isPrime):
        number = random.getrandbits(len-1) 
        number += 1<<(len-1)
        if(number % 2 == 0):
            continue
        else:
            isPrime = MillerRabin(number, 18)
    return number


def extendEuclid(a,b): 
    if(b==0):
        return 1,0, a
    x2, y2, remainder = extendEuclid(b,a%b) #Euclid for gcd
    
    x1 = y2
    y1 = x2 - (a//b)*y2

    return x1, y1, remainder 


def quickPowNMod(M, e, N):
    C = 1
    while(e!=0):
        if(e&1):
            C = (C*M)%N
        e >>= 1
        M = (M*M)%N
    return C


def pack(message):
    M = 0
    i = len(message) - 1
    for x in message:
        M += int(ord(x)) << (8 * i)
        i -= 1
    return M


def unpack(M):
    message = ""
    while(M != 0):
        x = M % (1 << 8)
        M = M // (1 << 8)
        message = chr(x) + message
    return message


key_size = int(input("Please input your key size (1024 and 2048 recommended):"))

reGen = True
while(reGen):

    lenP = random.randint(key_size//4,key_size//7*3)
    lenQ = key_size - lenP
    P = PQGenerate(lenP)
    Q = PQGenerate(lenQ)

    N = P*Q
    phi_N = (P-1)*(Q-1)
    if(N.bit_length()!=key_size):
        continue #reGen

    e = 65537
    if(phi_N%e==0):
        continue #reGen
    
    d = (extendEuclid(phi_N,e)[1] + phi_N) % phi_N
    if((e*d)%phi_N!=1):
        continue #reGen

    reGen = False


print("public key = (", e , ",", N,")\n")
print("private key = (", d , ",", N,")\n")

message = ""
while(message==""):
    message = input("Please input your message:\n")
print("")

encrypted = quickPowNMod(pack(message),e,N)
print("encrypted =", encrypted,"\n")

decrypted = unpack(quickPowNMod(encrypted,d,N))
print("decrypted =", decrypted)

"""
reGen = True
while(reGen):
    lenP = random.randint(300,450)
    lenQ = 1024 - lenP
    
    print("--Generating P...")
    P = PQGenerate(lenP)
    print(P)
    print("length of P:", P.bit_length(), "\n")
    
    print("--Generating Q...")
    Q = PQGenerate(lenQ)
    print(Q)
    print("length of Q:", Q.bit_length(), "\n")
        
    print("--computing N and phi N...")
    N = P*Q
    phi_N = (P-1)*(Q-1)
    print(N)
    print("length of N:",N.bit_length())
    if(N.bit_length()!=1024):
        continue #reGen
    
    print("--testing if e and phi N are relatively prime...\n")
    e = 65537
    if(phi_N%e==0):
        continue #reGen
    
    print("--computing d...")
    d = (extendEuclid(phi_N,e)[1] + phi_N) % phi_N
    print(d)
    if((e*d)%phi_N==1):
        print("valid d.\n")

    reGen = False
   
message = "we pretend the night won't steal our youth"

C = quickPowNMod(pack(message),e,N)
print("C:\n",C)

message2 = unpack(quickPowNMod(C,d,N))

print("M2:\n",message2)

"""
"""
cnt = 0
cnt1 = 0
cnt2 = 0
while(cnt<100):
    lenP = random.randint(300,450)
    lenQ = 1024 - lenP
    P = PQGenerate(lenP)
    Q = PQGenerate(lenQ)
    N = P*Q
    if(N.bit_length()==1024):
        cnt1 += 1
    elif(N.bit_length()==1023):
        cnt2 += 1
    cnt += 1
    print(cnt)

print("CNT 1024:", cnt1)
print("CNT 1023:", cnt2)
"""
