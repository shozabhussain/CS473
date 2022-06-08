import sys
import Crypto
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


with open("3.1.4_aes_weak_ciphertext.hex") as f:
    cypherText = f.read().strip()
f.close()

with open("3.1.4_aes_iv.hex") as f:
    iv = f.read().strip()
f.close()

with open("key11.hex") as f:
    key = f.read().strip()
f.close()

combinations = ["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13",
                "14","15","16","17","18","19","1a","1b","1c","1d","1e","1f"]

key  = "00000000000000000000000000000000000000000000000000000000000000"

for combination in combinations:

    cipher = AES.new( bytes.fromhex(key+combination), AES.MODE_CBC,  bytes.fromhex(iv))
    plaintext = cipher.decrypt( bytes.fromhex(cypherText))
    ##print(plaintext)

key1 = "000000000000000000000000000000000000000000000000000000000000001e"  ##this seems to give the correct answer
cipher = AES.new( bytes.fromhex(key1), AES.MODE_CBC,  bytes.fromhex(iv))
plaintext = cipher.decrypt( bytes.fromhex(cypherText))

f = open("sol_3.1.4.hex", 'w')
f.write(key1)
f.close()