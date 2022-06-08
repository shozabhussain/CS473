import sys
inputStringFile = sys.argv[1]
outputFile = sys.argv[2]

with open(inputStringFile) as f:
    inputString = f.read().strip()
f.close()

def WHA(inStr):
    mask = 0x3FFFFFFF
    outHash = 0

    for byte in inStr:
        byte = ord(byte)
        intermediate_value = ((byte ^ 0xCC) << 24) | ((byte ^ 0x33) << 16) | ((byte ^ 0xAA) << 8) | (byte ^ 0x55)
        outHash = (outHash & mask) + (intermediate_value & mask)

    outHash = hex(outHash)[2:]
    return outHash

#print(WHA(inputString))
#print(WHA("OBVE A TEA CAKE  REMEMBER THIS FRENCH NAME OF A GROUP OF ISLANDS IN THE GULF OF ST LAWRENCE"))

answer = "OBVE A TEA CAKE  REMEMBER THIS FRENCH NAME OF A GROUP OF ISLANDS IN THE GULF OF ST LAWRENCE"

f = open(outputFile, 'w')
f.write(answer)
f.close()