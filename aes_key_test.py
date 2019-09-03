import random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def bin2str(b):
    s = ""
    for i in range(0,len(b),8):
        s = s + chr(int(b[i:i+8],2))
    return s

aes_key1 = "0123012301230123"
crypto1 = AES.new(aes_key1, AES.MODE_ECB)
c1 = crypto1.encrypt("messagemessage12")
d1 = crypto1.decrypt(c1)
print(d1,"\n")

aes_key2 = bin2str("0"*128)
crypto2 = AES.new(aes_key2, AES.MODE_ECB)
c2 = crypto2.encrypt("messagemessage12")
d2 = crypto2.decrypt(c2)
print(d2,"\n")
"""
aes_key3 = bin2str("1"+"0"*127)
crypto3 = AES.new(aes_key3, AES.MODE_ECB)
c3 = crypto3.encrypt("messagemessage12")
d3 = crypto3.decrypt(c3)
print(d3,"\n")
"""
aes_key4 = bin2str("0"+"1"+"0"*126)
crypto4 = AES.new(aes_key4, AES.MODE_ECB)
c4 = crypto4.encrypt("messagemessage12")
d4 = crypto4.decrypt(c4)
print(d4,"\n")

aes_key5 = bin2str("00000000"+"1"+"0"*119)
crypto5 = AES.new(aes_key5, AES.MODE_ECB)
c5 = crypto5.encrypt("messagemessage12")
d5 = crypto5.decrypt(c5)
print(d5,"\n")
