import pymd5
import sys
import re
import urllib.parse

queryFile = sys.argv[1]
cmdFile = sys.argv[2]
outputFile = sys.argv[3]

with open(queryFile) as f:
    query = f.read().strip()
f.close()

with open(cmdFile) as f:
    cmd = f.read().strip()
f.close()

query = re.split('(&user)', query)

hashList = query[0]
hashList = re.split('(=)', hashList)
oldHash = hashList[2]
#print(oldHash)

h = pymd5.md5(state=oldHash, count=512)
h.update(cmd)
updatedHash = h.hexdigest()
#print(updatedHash)

oldQuery = query[1]+ query[2]
oldQuery = oldQuery[1:]

lenOldQuery = len(oldQuery) + 8   ## 8 because of the password
#print(lenOldQuery)

paddingToAdd = pymd5.padding(lenOldQuery*8)
paddingToAdd = urllib.parse.quote_from_bytes(paddingToAdd)
#print(paddingToAdd)

modifiedURL = hashList[0] + hashList[1] + updatedHash + "&" + oldQuery + paddingToAdd + cmd
#print(modifiedURL)

f = open(outputFile, 'w')
f.write(modifiedURL)
f.close()

