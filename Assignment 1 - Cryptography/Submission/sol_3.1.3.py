import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

cypherTextFile = sys.argv[1]
keyFile = sys.argv[2]
ivFile = sys.argv[3]
outputFile = sys.argv[4]

with open(cypherTextFile) as f:
    cypherText = f.read().strip()
f.close()

with open(keyFile) as f:
    key = f.read().strip()
f.close()

with open(ivFile) as f:
    iv = f.read().strip()
f.close()


cipher = AES.new( bytes.fromhex(key), AES.MODE_CBC,  bytes.fromhex(iv))
plaintext = cipher.decrypt( bytes.fromhex(cypherText))

f = open("sol_3.1.3.txt", 'w')
f.write(str(plaintext)[2:])
f.close()