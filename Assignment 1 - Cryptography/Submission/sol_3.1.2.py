import sys
cypherTextFile = sys.argv[1]
keyFile = sys.argv[2]
outputFile = sys.argv[3]

with open(cypherTextFile) as f:
    cypherText = f.read().strip()

with open(keyFile) as f:
    key = f.read().strip()

keyDict = {}

for i in range(26):
    keyDict[key[i]] = chr(65+i)

keyDict[" "] = " "

for i in range(10):
    keyDict[chr(48+i)] = chr(48+i)


plaintext = ""

for i in range(len(cypherText)):
    plaintext = plaintext + keyDict[cypherText[i]]

f = open("sol_3.1.2.txt", 'w')
f.write(plaintext)
f.close()