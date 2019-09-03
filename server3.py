import random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import socket


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
        number += 1 << (len-1)
        if(number % 2 == 0):
            continue
        else:
            isPrime = MillerRabin(number, 18)
    return number


def extendEuclid(a, b):
    if(b == 0):
        return 1, 0, a
    x2, y2, remainder = extendEuclid(b, a % b)  # Euclid for gcd

    x1 = y2
    y1 = x2 - (a//b)*y2

    return x1, y1, remainder


def quickPowNMod(M, e, N):
    C = 1
    while(e != 0):
        if(e & 1):
            C = (C*M) % N
        e >>= 1
        M = (M*M) % N
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



key_size = 1024

reGen = True
while(reGen):

    lenP = random.randint(key_size//4, key_size//7*3)
    lenQ = key_size - lenP
    P = PQGenerate(lenP)
    Q = PQGenerate(lenQ)

    N = P*Q
    phi_N = (P-1)*(Q-1)
    if(N.bit_length() != key_size):
        continue  # reGen

    e = 65537
    if(phi_N % e == 0):
        continue  # reGen

    d = (extendEuclid(phi_N, e)[1] + phi_N) % phi_N
    if((e*d) % phi_N != 1):
        continue  # reGen

    reGen = False


print "public key = (", e, ",", N, ")"
print "private key = (", d, ",", N, ")","\n"

aes_key = raw_input("Feel free to set your aes key (16 characters):")
while(len(aes_key)!=16):
    print "I said we need 16 characters!"
    aes_key = raw_input("Input again:")
print "aes key =", aes_key, "\n"

encrypted = quickPowNMod(pack(aes_key), e, N)
print "encrypted aes_key =", encrypted, "\n"

cryptos = AES.new(aes_key, AES.MODE_ECB)
history_encrypted_wup = cryptos.encrypt("WUP0WUP1WUP2WUP3")
print "encrypted WUP request in utf-8: ", b2a_hex(history_encrypted_wup).decode("utf-8"), "\n"


# sock
byte = 1024
port = 25535
host = ""
addr = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(addr)
print "waiting for a client..."

msg = ""
while(msg != "Let's get it started"):
    (data, addr) = sock.recvfrom(byte)
    msg = data.decode("utf-8")

print "found a client. Sending rsa pk and encrypted aes key..." 
data_N = str(N).encode("utf-8")
data_encrypted_aes_key = str(encrypted).encode("utf-8")
data_history_encrypted_wup = b2a_hex(history_encrypted_wup)
sock.sendto(data_N, addr)
sock.sendto(data_encrypted_aes_key, addr)
sock.sendto(data_history_encrypted_wup, addr)

while(True):
    (data_C, addr) = sock.recvfrom(byte)
    (data_encrypted_wup, addr) = sock.recvfrom(byte)
    C = data_C.decode("utf-8")
    encrypted_wup = data_encrypted_wup.decode("utf-8")
    print "encrypted wup:", encrypted_wup
    if(C == "end"):
        break
    else:
        decrypted_C = unpack(quickPowNMod(int(C), d, N))[-16:]
        pack_C = quickPowNMod(int(C), d, N) % (1<<128)
        cryptos2 = AES.new(decrypted_C, AES.MODE_ECB)
        decrypted_wup = cryptos2.decrypt(a2b_hex(encrypted_wup))
        decrypted_wup_ref = cryptos.decrypt(a2b_hex(b2a_hex(history_encrypted_wup).decode("utf-8")))
        if(decrypted_wup == decrypted_wup_ref):
            msg = "valid".encode("utf-8")
        else:
            msg = "invalid".encode("utf-8")
        
        sock.sendto(msg, addr)
        print "Client just sent a/an", msg, "message!"
