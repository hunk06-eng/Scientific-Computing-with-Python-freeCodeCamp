import secrets
import re

# secrets module is more secure than random. random module outputs can be predicted.
# re stands for RegularExpression
# the regular expression I used in here is not necessary, there's no need to check the generated password everytime
# but this is an educational repo, so why not add it?

def generate_password(password_len = 16, alphabet_len = 10, digits_len = 4, symbols_len = 2):
    strings = {
        "letter": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digits": "0123456789",
        "symbols": "-?!@#$%^&*()_+="
    }
    # finds the actual total vs. the password length the user passed to the function
    # if the actual total is less, the script will automatically compensate by adding the difference to the amount letters
    real_total = alphabet_len+digits_len+symbols_len
    if real_total != password_len:
        print("Warning! Difference found between the sum of specified lengths and requested password length!")
        print("Increasing the amount of letters in password to account for difference...")
        alphabet_len += password_len-real_total

    # in the regex, I used ( {{{ }}} ) three brackets because im using both a raw-string and an f-string.
    # one bracket is used for the f-string ( {} ), the other one needs to be escaped for the regex ( {{ }} )
    # fun fact, if you add a dash like this in the character class: [?@!-#$%]
    # the dash in the middle is not treated as a literal character
    # instead the character class uses it to create a range between two characters by their ASCII code
    # so, to avoid unexpected behavior, place the dash at the beginning of the class [-...] or at the end [...-]

    check = re.compile(rf"[a-zA-Z]{{{alphabet_len}}}[0-9]{{{digits_len}}}[-?!@#$%^&*()_+=]{{{symbols_len}}}")
    alphabet_len_c, digits_len_c, symbols_len_c = 0, 0, 0 # to keep track of how many characters were added.
    password = ["", "", ""] # [0] represents letters, [1] represents digits, [2] represents symbols
    for run in range(password_len):
        # here, im using secrets to generate random values (indexes, in this case) below the length of each category
        if alphabet_len != alphabet_len_c:
            password[0] += strings["letter"][secrets.randbelow(52)] # 26 small letters, 26 capital letters
            alphabet_len_c += 1
        if digits_len != digits_len_c:
            password[1] += strings["digits"][secrets.randbelow(10)] # 0 - 9 are 10 digits total
            digits_len_c += 1
        if symbols_len != symbols_len_c:
            password[2] += strings["symbols"][secrets.randbelow(15)] # script supports up to 15 symbols
            symbols_len_c += 1

    password_str_version = "".join(password)
    if bool(check.match(password_str_version)): # an extra sanity check before shuffle
        # calling the mixer function
        # it's very important, it shuffles each character in a random place
        # if we don't use it, we will have all letters, followed by all digits, followed by all symbols in order
        # which is not good for generating a password.
        return f"Your generated password : {mixer(password_str_version)}"
    else:
        print("Error! Terminating...")
        return None

def mixer(password_str_ver):
    pass_index = list(range(len(password_str_ver))) # creating a list of the indexes of the password
    mixed = "" # a new string to place the shuffled characters
    while len(mixed) != len(password_str_ver): # only stop when the mixed string equals the original password in length
        random_val = secrets.choice(pass_index) # choosing a random value from the indexes list
        # removing the random value we picked from the original list so it is not used again
        # very important to ensure the script doesn't add duplicates by accident to the new shuffled string
        pass_index.remove(random_val)
        mixed += password_str_ver[random_val]
    return mixed

print(generate_password())

if __name__ == "__main__":
    print("\n-- Password generator! --")
    print("-- Not a cryptography expert, please use for educational purposes only! --")
    print("-- Input [N] at the end to exit script. --\n")

    while True:
        try:
            pass_len = int(input("Enter length of generated password: ").strip())
            remaining_chars = pass_len
            alpha_len = int(input("Enter number of letters to generate in password: ").strip())
            remaining_chars -= alpha_len
            print(f"{remaining_chars} left!")
            dig_len = int(input("Enter number of digits to generate in password: ").strip())
            remaining_chars -= dig_len
            print(f"{remaining_chars} left!")
            sym_len = int(input("Enter number of symbols to generate in password: ").strip())
            remaining_chars -= sym_len
            print(f"{remaining_chars} left!")
        except ValueError:
            print("Only accepts integer numbers for input... Please try again and enter digits only.")
            continue

        if pass_len < 0:
            print("Error! Password length cannot be negative. Please try again...\n")
            continue
        if (alpha_len+dig_len+sym_len) > pass_len:
            print("Error! Specified lengths are longer than the requested password length!\nPlease try again...\n")
            continue
        if (alpha_len<0) or (dig_len<0) or (sym_len<0):
            print("Can't accept negative lengths! I don't owe you characters bro...")
            print("Please try again... Only positive numbers or zero.\n")
            continue

        print("\n")
        print(generate_password(pass_len, alpha_len, dig_len, sym_len))

        continue_status = input("Continue? [Y] for yes | [N] for no : ").strip()
        if continue_status.upper() == 'N':
            print("Exiting script...")
            break