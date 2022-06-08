import sagemath
import functools
import math
from Crypto.Util import number
import pbp
from Crypto.PublicKey import RSA

with open("moduli.hex") as f:
    moduli = f.readlines()
f.close()

with open("3.2.3_ciphertext.enc.asc") as f:
    cypher_txt= f.read()
f.close()

count = 0
for i in moduli:
  moduli[count] = int(moduli[count],16)
  count +=1

## code for product tree and batchgcd taken from here: https://facthacks.cr.yp.to/batchgcd.html
# def producttree(X):
#        result = [X]
#        while len(X) > 1:
#          X = [math.prod(X[i*2:(i+1)*2]) for i in range(((len(X)+1)//2))]
#          result.append(X)
#        return result

# def batchgcd_faster(X):
#   prods = producttree(X)
#   R = prods.pop()
#   while prods:
#     X = prods.pop()
#     R = [R[int(i//2)] % X[i]**2 for i in range(len(X))]

#   return [math.gcd((r//n), n) for r,n in zip(R,X)]

# gcds = batchgcd_faster(moduli)

# f = open("calculated_gcds.txt", 'w')

# for l in gcds:
#   f.writelines(str(l)+'\n')
# f.close()

with open("calculated_gcds.txt") as f:
    gcds = f.readlines()
f.close()

count = 0
for i in gcds:
  gcds[count] = int(gcds[count])
  count +=1

pAndq = []
count = 0
for i in gcds:

  if gcds[count] != 1:
    pAndq.append((gcds[count], moduli[count]//gcds[count]))

  count = count +1

print(pAndq[0])
def get_d(p, q, e):
 totient = (p-1)*(q-1)
 return number.inverse(e,totient)

secretKeys = []
for pair in pAndq:
  secretKeys.append(get_d(pair[0], pair[1],  65537))

count = 0
for d in secretKeys:
    n = pAndq[count][0] * pAndq[count][1]
    try:
        key = RSA.construct((n, 65537, d))
        plaintext = pbp.decrypt(key, cypher_txt)
        print(plaintext)
        count = count + 1
    except:
        count = count + 1
        continue

f = open("sol_3.2.3.txt", 'w')
f.write(str(plaintext))
f.close()