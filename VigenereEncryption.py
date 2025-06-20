print("*\n*\n*")
print("DO NOT USE this encryption method for ANY sensitive data.\n")
print("*\n*\n*\n")

def vigenere(text, key, mode=1):
    final_message = ''
    key_loc = 0
    
    for char in text:
        # pass any symbols, numbers, punctuation marks without encrypting/decrypting them.
        if char.isalpha() == False:
            final_message += char

        else:
            # find index of char using ascii table
            char_index = (ord(char)-65) if char.isupper() else (ord(char)-97)
            # key_loc keeps track of which letter (in the key) the iteration stopped at during encryption/decryption process.
            # modulo is used to circle through the key once the key_loc variable exceeds the key's length.
            key_index = (ord(key[key_loc % len(key)])-65) if key[key_loc % len(key)].isupper() else (ord(key[key_loc % len(key)]) - 97)
            key_loc += 1

            # same as before, modulo ensures that the rotation circles back to the start of the alphabet once it exceeds it's length.
            rotation = (char_index+key_index*mode) % 26

            final_message += get_char_by_index(rotation, char.isupper())
    return final_message

def get_char_by_index(rotation, isUpper):
    # using the ascii table, if the character in the text is uppercase, add the rotation amount to 'A' -- > 65 on ascii table, then convert integer to character.
    # if the character in the text is lowercase, add the rotation mount to 'a' -- > 97 on ascii table, then convert integer to character using chr().

    return (chr(65+rotation) if isUpper else chr(97+rotation))

# while loop so the script runs as many times as needed.
while True:
    text = input('Enter the text you want to encrypt/decrypt: ')
    key = input('Enter the key to use for encryption/decryption: ')
    mode = int(input('Enter 1 for encryption, -1 for decryption: '))

    if len(key) == 0:
        key = input('Please enter a key for the script to proceed: ')

    print(vigenere(text, key, mode))

    print("\nEnter 0 to restart script, 1 to close it.")
    if int(input()):
        break
    
    print('\n')
