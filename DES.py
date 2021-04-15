from sys import exit
from time import time

flen=4
sukey_len=8
key_len=10
datalen=8

# Tables for initial and final permutationnutations (b1, b2, b3, ... b8)
FPtable=(4,1,3,5,7,2,8,6)
IPtable=(2,6,3,1,4,8,5,7) 
# Tables for sukey generation (k1, k2, k3, ... k10)
P8table=(6,3,7,4,8,5,10,9)
P10table=(3,5,2,7,4,10,1,9,8,6)
# Tables for the fk function
EPtable=(4,1,2,3,2,3,4,1)
P4table=(2,4,3,1)
S1table=(0,1,2,3,2,0,1,3,3,0,1,0,2,1,0,3)
S0table=(1,0,3,2,3,2,1,0,0,2,1,3,3,1,3,2)
 
def permutationn(inByte,perTable):
    """permutationnute input byte according to permutationnutation table"""
    outByte=0
    for index,ele in enumerate(perTable):
        if index >= ele:
            outByte |= (inByte & (128 >> (ele - 1))) >> (index - (ele - 1))
        else:
            outByte |= (inByte & (128 >> (ele - 1))) << ((ele - 1) - index)
    return outByte
 
def ip(inByte):
    """Perform the initial permutationnutation on data"""
    return permutationn(inByte,IPtable)
 
def fp(inByte):
    """Perform the final permutationnutation on data"""
    return permutationn(inByte,FPtable)
 
def swapNibbles(inByte):
    """Swap the two nibbles of data"""
    return (inByte << 4 | inByte >> 4) & 0xff
 
 
def keyGen(key):
    """Generate the two required sukeys"""
    def left_shiftt(keyBitList):
        """Perform a circular left shift on the first and second five bits"""
        shftkey=[None] * key_len
        shftkey[0:9]=keyBitList[1:10]
        shftkey[4]=keyBitList[0]
        shftkey[9]=keyBitList[5]
        return shftkey
 
    # Converts input key (integer) into a list of binary digits
    keyList=[(key & 1 << i) >> i for i in reversed(range(key_len))]
    permutationnKeyList=[None] * key_len
    for index, elem in enumerate(P10table):
        permutationnKeyList[index]=keyList[elem - 1]
    shonekey=left_shiftt(permutationnKeyList)
    shtwkey=left_shiftt(left_shiftt(shonekey))
    sukey1=sukey2=0
    for index, elem in enumerate(P8table):
        sukey1 += (128 >> index) * shonekey[elem - 1]
        sukey2 += (128 >> index) * shiftedTwiceKey[elem - 1]
    return (sukey1, sukey2)


def fk(sukey, inputData):
    """Apply Feistel function on data with given sukey"""
    def F(sKey, rightNibble):
        aux=sKey ^ permutationn(swapNibbles(rightNibble), EPtable)
        in2=((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                 ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
        in1=((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                 ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
        sboxOutputs=swapNibbles((S0table[in1] << 2) + S1table[in2])
        return permutationn(sboxOutputs, P4table)
 
    leftNibble,rightNibble=inputData & 0xf0, inputData & 0x0f
    return (leftNibble ^ F(sukey, rightNibble)) | rightNibble
 

def encrypt(key, plaintext):
    """Encrypt plaintext with given key"""
    data=fk(keyGen(key)[0], ip(plaintext))
    return fp(fk(keyGen(key)[1], swapNibbles(data)))
 

def decrypt(key, ciphertext):
    """Decrypt ciphertext with given key"""
    data=fk(keyGen(key)[1], ip(ciphertext))
    return fp(fk(keyGen(key)[0], swapNibbles(data)))  
 

if __name__ == '__main__':
 
    try:
        assert encrypt(0b0000000000, 0b10101010) == 0b00010001
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b0000000000, 0b10101010), "Expected: ", 0b00010001)
        exit(1)
    try:
        assert encrypt(0b1110001110, 0b10101010) == 0b11001010
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1110001110, 0b10101010), "Expected: ", 0b11001010)
        exit(1)
    try:
        assert encrypt(0b1110001110, 0b01010101) == 0b01110000
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1110001110, 0b01010101), "Expected: ", 0b01110000)
        exit(1)
    try:
        assert encrypt(0b1111111111, 0b10101010) == 0b00000100
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1111111111, 0b10101010), "Expected: ", 0b00000100)
        exit(1)
 
    t1=time()
    for i in range(1000):
        encrypt(0b1110001110, 0b10101010)
    t2=time()
    print("Elapsed time for 1000 encryptions: {:0.3f}s".format(t2 - t1))
    exit()