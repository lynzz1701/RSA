from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import socket

def quickPowNMod(M, e, N):
    C = 1
    while(e != 0):
        if(e & 1):
            C = (C*M) % N
        e >>= 1
        M = (M*M) % N
    return C
 

def bin2str(b):
    s = ""
    for i in range(0,len(b),8):
        s = s + chr(int(b[i:i+8],2))
    return s


host = "192.168.146.128"    

port = 25535
addr = (host, port)
byte = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = ""
while(msg != "Let's get it started"):
    msg = raw_input("Shall we start?\n")
    sock.sendto(msg.encode("utf-8"), addr)

e = 65537
(data_N, addr) = sock.recvfrom(byte)
(data_encrypted_aes_key, addr) = sock.recvfrom(byte)
(data_history_encrypted_wup, addr) = sock.recvfrom(byte)
N = int(data_N.decode("utf-8"))
C = int(data_encrypted_aes_key.decode("utf-8"))

print "I got N:", N,"\n"
print "I got C:", C,"\n"
current_known = ""
for b in range(127,-1,-1):
    print "*"*60
    print "b=",b
    C_b = (C * quickPowNMod(2,b*e,N)) % N
    aes_key_b = "0" + current_known + "0"*b
    print "try this key:",aes_key_b,"\n"
    aes_key_b = bin2str(aes_key_b)
    crypto = AES.new(aes_key_b, AES.MODE_ECB)
    encrypted_wup = crypto.encrypt("WUP0WUP1WUP2WUP3")
    
    data_C_b = str(C_b).encode("utf-8")
    data_encrypted_wup = b2a_hex(encrypted_wup)
    sock.sendto(data_C_b, addr)
    sock.sendto(data_encrypted_wup, addr)

    (data_msg, addr) = sock.recvfrom(byte)
    msg = data_msg.decode("utf-8")
    if(msg=="valid"):
        current_known = "0" + current_known
    else:
        current_known = "1" + current_known
    print "current known aes key:", current_known,"\n"

print "I guess the aes_key is:", bin2str(current_known)

crypto_aes_key = AES.new(bin2str(current_known),AES.MODE_ECB)
history_decrypted_wup = crypto_aes_key.decrypt(a2b_hex(data_history_encrypted_wup.decode("utf-8"))).decode("utf-8")
print "decrypt from history wup:", history_decrypted_wup




