import textwrap
try:
    import readline
except ImportError: # Only available on POSIX, but no big deal.
    pass

def initialize(key):
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

def loop_user_query(k):
    """Raises EOFError when the user uses an EOT escape sequence (i.e. ^D)."""
    quotes = "'\""
    while True:
        text = raw_input('Enter plain or cipher text: ')
        if text[0] == text[-1] and text[0] in quotes: #Assume text is ciphered if it is in quotes to start
            # Unescape presumed ciphertext.
            print 'Unescaping ciphertext...'
            text = text[1:-1].decode('string_escape') #Makes the passed in text back into a string
        k_copy = list(k)
        print 'Your RC4 text is:', repr(runRC4(k_copy, text))  #Passing encoded text into RC4, with the same key, will unencode it
        print
 
 
def print_prologue():
    title = 'RC4 Utility'
    print '=' * len(title)
    print title
    print '=' * len(title)
    explanation = """The output values are valid Python strings. They may
contain escape characters of the form \\xhh to avoid confusing your terminal
emulator. Only the first 256 characters of the encryption key are used."""
    for line in textwrap.wrap(explanation, width=79):
        print line
    print
 
 
def main():
    """Present a command-line interface to the cipher."""
    print_prologue()
    # Acquire initial cipher values.
    key = raw_input('Enter an encryption key: ')
    print
    key = [ord(char) for char in key]
    k = initialize(key)
    # Perform cipher until exit.
    try:
        loop_user_query(k)
    except EOFError:
        print
        print 'Have a pleasant day!'
 
 
if __name__ == '__main__':
    main()
