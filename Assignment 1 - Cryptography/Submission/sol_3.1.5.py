import sys
cypherTextFile = sys.argv[1]
keyFile = sys.argv[2]
moduloFile = sys.argv[3]
outputFile = sys.argv[4]

with open(cypherTextFile) as f:
    cypherText = f.read().strip()
f.close()

with open(keyFile) as f:
    key = f.read().strip()
f.close()

with open(moduloFile) as f:
    modulo = f.read().strip()
f.close()

plaintext = int(cypherText, 16)**int(key, 16)
plaintext = plaintext % int(modulo,16)
plaintext = hex(plaintext)[2:]

f = open(outputFile, 'w')
f.write(plaintext)
f.close()
