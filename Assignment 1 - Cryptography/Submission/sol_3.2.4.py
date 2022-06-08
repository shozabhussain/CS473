from Crypto.Util import number
import math

with open("output.cer", 'rb') as f:
    IV = f.read(260)
f.close()

f = open("IV.hex", 'w')
f.write(IV.hex()[8:])
f.close()

with open("col1", 'rb') as f:
    b1 = f.read()
f.close()

with open("col2", 'rb') as f:
    b2 = f.read()
f.close()

b1 = b1.hex()[-256:]
b1 = int(b1, 16)

b2 = b2.hex()[-256:]
b2 = int(b2, 16)

def generatePrime():

    while(1):
        p = number.getPrime(500)
        if math.gcd((p-1), 65537) == 1:
            return p

p1 = generatePrime()
p2 = generatePrime()

b1_exp = b1*(2**1024)
b2_exp = b2*(2**1024)

def getCRT(b1_exp, b2_exp, p1, p2):
 N = p1 * p2
 invOne = number.inverse(p2, p1)
 invTwo = number.inverse(p1, p2)
 return -(b1_exp * invOne * p2 + b2_exp * invTwo * p1) % N

b0 = getCRT(b1_exp, b2_exp, p1, p2)

k = 0
b = 0
q1 = 0
q2 = 0
while(1):
    if k%100000 == 0:
        print(k)
    b = b0 + (k*p1*p2)
    q1 = (b1*(2**1024) + b)//p1
    q2 = (b2*(2**1024) + b)//p2
    if number.isPrime(q1) == True and number.isPrime(q2) == True and math.gcd((q1-1), 65537) == 1 and math.gcd((q2-1), 65537) == 1:
        break
    elif b >= (2**1024):
        print("exceeded")
        break
    else:
        k = k + 1

n1 = b1*(2**1024) + b
n2 = b2*(2**1024) + b

print("p1 = ", p1, '\n')
print("p2 = ", p2, '\n')
print("q1 = ", q1, '\n')
print("q2 = ", q2, '\n')
print("b = ", b, '\n')

## we will now use these p1 q1 and p2 q2 to generate two certificates with same serial number using certbuilder.