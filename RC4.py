def intialize(key):
    """
    This will generate a 256 entry list list
    Indices can not be greater than 255
    """
    k = range(256)                                #If only the stop value is given, range will assume start == 0, step through by 1
    j = 0
    for i in range(256):
        j = (j + k[i] + key[i % len(key)]) % 256  #Remember that percent sign can be used as mod,
                                                  #returns remainder from a division
        k[i],k[j] = k[j],k[i]                     #Swap the ith and jth indices
    return k                                      #return the 256 entry list k which has been swapped about

def genRandomBytes(k):
    """
    Generates a pseudo-random set of bytes based on scrambled list k
    Builds the list in "real-time" rather than one giant block to start
    which is computationally more efficient"""
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + k[i]) % 256                      #Scrambles j again
        k[i],k[j] = k[j],k[i]                     #Swap the ith and jth indices again
        yield k[(k[i] + k[j]) % 256]              #Generate a new

def runRC4(k, text):
    """
    This function performs the actual encryption of "actual" text
    """
    cipherChars = []                              #Empty array
    randomByteGen = genRandomBytes(k)             #Builds a new genRandomBytes passing in list k
    for char in text:                             #Iterate through text and grab each charecter
        byte = ord(char)                          #Ord returns the integer representing the uncode of a charecter
        cipherByte = byte ^ randomByteGen.next()  #Generate a new random byte, XOR the integer representing text charecter with this random byte
        cipherChars.append(chr(cipherByte))       #Turn it back into a char and put it in the array
    return ''.join(cipherChars)                   #Return the array
