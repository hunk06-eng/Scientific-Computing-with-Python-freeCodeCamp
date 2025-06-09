print("*\n*\n*")
print("It is not recommended to use this encryption method for sensitive data, in the past, vigenere encryption was hard to break; but with computers it became easier to crack, this code is recommended for educational purposes only.\n")
print("*\n*\n*\n")

text = input('Enter the text you want to encrypt/decrypt: ')
key = input('Enter the key to use for encryption/decryption: ')
mode = int(input('Enter 1 for encryption, -1 for decryption: '))

if len(key) == 0:
    key = input('Please enter a key for the script to proceed: ')

alphabet_index = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 'r':17, 's':18,
            't':19, 'u':20, 'v':21, 'w':22, 'x':23, 'y':24, 'z':25, 'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11,
            'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17, 'S':18,'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25}

def vigenere(text, key, mode=1):
    global alphabet_index
    final_message = ''
    key_loc = 0
    
    for char in text:
        # pass any symbols, numbers, punctuation marks without encrypting/decrypting them.
        if char not in alphabet_index:
            final_message += char
        else:
            # find index of char
            char_index = alphabet_index[char]
            # key_loc keeps track of which letter (in the key) the iteration stopped at during encryption/decryption process.
            # modulo used to circle through the start of the key once the key_loc variable exceeds the key's length.
            key_index = alphabet_index[key[key_loc % len(key)]]
            key_loc += 1

            # same as before, modulo ensures that the rotation circles back to the start of the alphabet once it exceeds it's length.
            rotation = (char_index+key_index*mode) % 26

            final_message += get_char_by_index(rotation, char.isupper())
    return final_message

def get_char_by_index(index, isUpper):
    global alphabet_index

    for char, indx in alphabet_index.items():
        if indx == index:
            if isUpper:
                return char.upper()
            else:
                return char

print(vigenere(text, key, mode))
input("\nPress enter to exit.")