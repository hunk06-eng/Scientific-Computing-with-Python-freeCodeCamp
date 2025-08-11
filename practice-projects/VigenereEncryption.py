print("****")
print("DO NOT USE this encryption method for ANY sensitive data.")
# 81 stands for Q and 84 stands for T in ASCII, didn't use Q or T to avoid reserving them for the script.
print("To quit the script at any time, enter the number 81")
print("To run test cases, enter the number 84 (AT KEY PROMPT ONLY)")
print("****")


def vigenere(text, key, mode=1):
    final_message = ''
    key_loc = 0
    
    for char in text:
        # pass any symbols, numbers, punctuation marks without encrypting/decrypting them.
        if not char.isalpha():
            final_message += char

        else:
            # find index of char using ascii table
            char_index = (ord(char)-65) if char.isupper() else (ord(char)-97)
            """
            key_loc keeps track of which letter (in the key) the iteration stopped at during an encryption/decryption process.
            modulo is used to circle through the key once the key_loc variable exceeds the key's length.
            """
            key_index = (ord(key[key_loc % len(key)])-65) if key[key_loc % len(key)].isupper() else (ord(key[key_loc % len(key)]) - 97)
            key_loc += 1

            # same as before, modulo ensures that the rotation circles back to the start of the alphabet once it exceeds it's length.
            rotation = (char_index+key_index*mode) % 26

            final_message += get_char_by_index(rotation, char.isupper())
    return final_message


def get_char_by_index(rotation, isUpper):
    """
    using the ascii table, if the character in the text is uppercase, add the rotation amount to 'A' -- > 65 on ascii table, then convert integer to character.
    if the character in the text is lowercase, add the rotation mount to 'a' -- > 97 on ascii table, then convert integer to character using chr().
    """

    return chr(65 + rotation) if isUpper else chr(97 + rotation)


def test_cases():
    # some default test cases to ensure everything is working as expected.
    test_cases_text = ["PotatoLover", "Potato Lover !@#", "", "Chaos(!@#$%^&**)&(-94239329)   WhiteSpaceHere $$$"]
    test_cases_key = ["HeLikesPotato", "WeGetItMan", "EmptyTestCase", "ThisIsAVeryVeryVeryLongLongLongLongLongLongLongLongKEY"]
    test_cases_mode = [1, -1, -1, 1]
    # actual expected result, computed by an alternative script.
    expected_result = ["WseidsDdjxr", "Tknwag Scvrv !@#", "", "Voiga(!@#$%^&**)&(-94239329)   OhdxvQketcCiic $$$"]
    # this variable is used to keep track of how many test cases passed.
    success = 0

    print("Testing Cases Now. You'll be notified if script output doesn't match expected output.\n")

    for idx, text in enumerate(test_cases_text):
        print(f"Evaluating test case number {idx+1}: {text} with the KEY {test_cases_key[idx]}")
        print(f"Mode is: {"Encryption" if test_cases_mode[idx] == 1 else "Decryption"}\n")
        res = vigenere(text, test_cases_key[idx], test_cases_mode[idx])
        if res == expected_result[idx]:
            print(f"expected result: {expected_result[idx]}, actual result: {res}\n")
            success += 1

    # once the for loop ends, ensure that successful test cases are equal to the total number of test cases evaluated.
    if success == len(test_cases_text):
        print("All test cases passed successfully! Everything is working as expected.")
    else:
        print(f"Something went wrong, only {len(test_cases_text) - success} cases passed.")

if __name__ == "__main__":
    def main():
        # while loop so the script runs as many times as needed.
        while True:
            print("\n")
            text_in = input("Enter the text you want to encrypt/decrypt: ")
            if text_in == "81": # if user wants to quit
                print("Exiting the script.")
                break

            key_in = input("Enter the key to use for encryption/decryption: ")
            if not key_in.isalpha(): # 81 and 84 both are invalid keys anyway, so we can check them in here.
                if key_in == "84": # if user wants to launch test cases
                    test_cases()
                    what_now = input("Enter Y to continue or N to stop: ")
                    if what_now == 'Y':
                        continue
                    elif what_now == 'N':
                        break
                elif key_in == "81": # if user want to quit
                    print("Exiting the script.")
                    break
                print("Invalid key, key must not contain any symbols/digits/spaces.")
                continue

            mode_in = input("Enter 1 for encryption, -1 for decryption: ")
            if mode_in not in ['1', '-1']:
                if mode_in == "81": # same concept as before, if mode_in is invalid, it could be the user entering 81 or 84.
                    print("Exiting the script.")
                    break
                print("Invalid mode baby girl, enter 1 for encryption, -1 for decryption.") # baby girl you didn't follow instructions
                continue

            print(vigenere(text_in, key_in, int(mode_in)))
            print('\n')

    main() # launching the script