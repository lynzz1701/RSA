import random
import hashlib

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


def i2osp(integer, size = 4):
    return "".join([chr((integer >> (8 * i)) & 0xFF) for i in reversed(range(size))])


def mgf(input, length, hash = hashlib.sha256):#based on SHA256
    counter = 0
    output = ""
    while(len(output) < length):
        C = i2osp(counter, 4)
        output += hash((str(input)+C).encode('utf-8')).hexdigest()
        counter += 1
    return int(output[:length],16)


def encrypt(messageBlock, e, N):
    #pack
    messageBlock = pack(messageBlock)

    #encode
    r = random.getrandbits(256) # k0 = 256
    messageBlock = messageBlock << 255 # k1 = 255
    digestG = mgf(r, 96)
    X = messageBlock^digestG
    digestH = mgf(X, 32)  
    Y = r^digestH
    W =  (X << 256) + Y
    
    #encrypt
    CBlock = quickPowNMod(W, e, N)

    return CBlock


def decrypt(CBlock, d, N):
    #decrypt
    W = quickPowNMod(CBlock, d, N)

    #decode
    X = W >> 256
    Y = W % (1 << 256)
    digestH = mgf(X, 32)
    r = Y^digestH
    digestG = mgf(r, 96)
    messageBlcok = X^digestG
    messageBlcok = messageBlcok >> 255 # k1 = 255
    
    #unpack
    messageBlcok = unpack(messageBlcok)
    
    return messageBlcok


reGen = True
while(reGen):

    lenP = random.randint(300,450)
    lenQ = 1024 - lenP
    P = PQGenerate(lenP)
    Q = PQGenerate(lenQ)

    N = P*Q
    phi_N = (P-1)*(Q-1)
    if(N.bit_length()!=1024):
        continue #reGen

    e = 65537
    if(phi_N%e==0):
        continue #reGen
    
    d = (extendEuclid(phi_N,e)[1] + phi_N) % phi_N
    if((e*d)%phi_N!=1):
        continue #reGen

    reGen = False

print("key size = 1024\n")
print("public key = (", e , ",", N,")\n")
print("private key = (", d , ",", N,")\n")

message = ""
while(message==""):
    message = input("Please input your message:\n")
print("")

"""
message = random.getrandbits(512)
print("message = ",message,"\n")
"""

encrypted = encrypt(message, e, N)
print("encrypted =", encrypted,"\n")

decrypted = decrypt(encrypted, d, N)
print("decrypted =", decrypted)
