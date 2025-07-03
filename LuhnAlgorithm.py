"""
    The Luhn algorithm is used to verify numbers in credit cards, SSN, etc.
    It multiplies every 2nd digit from the right to left by 2, if it's bigger than 9, it subtracts 9 from it and adds all numbers to the sum.
    If the sum % 10 == 0 (dividable by 10) then the number is valid [with the check digit included in sum], else It's invalid.
    It serves as a quick way to check for typos and errors.
"""
def luhn_number(num):
    if not num.isdigit() or len(num) < 2:
        return False

    total_sum = 0
    for idx, digit in enumerate(num):
        digit = int(digit)
        if idx % 2:
            digit *= 2
            total_sum += digit if digit<=9 else digit-9
        else:
            total_sum += digit
    return True if (total_sum % 10 == 0) else False

def test_cases():
    number_list = ["49927398716", "79927398713", "1234567812345670", "4012888888881881", "6011111111111117", "49927398717",
                   "79927398710", "1234567812345678", "4111111111111121", "6011111111111110", "0", "", "abcd1234", "059"]
    expected_result = [True, True, True, True, True, False, False, False, False, False, False, False, False, True]
    passed_cases = 0

    for idx, number in enumerate(number_list):
        if luhn_number(number[::-1]) == expected_result[idx]:
            passed_cases += 1
        else:
            print(f"{number} didn't pass.")

    return f"{len(number_list) - passed_cases} cases failed to pass."

def main():
    print("You can launch built-in test-cases by inserting [T] at the next prompt.")
    number = input("Enter number to verify using the Luhn Algorithm:")
    if number == 'T':
        return test_cases()
    non_digits_trans = str.maketrans("", "", "-_ ")
    number_translated = number.translate(non_digits_trans)[::-1]

    return "The number is valid!" if luhn_number(number_translated) else "The number is invalid!"

while True:
    print(main())
    usr_choice = input("\nEnter [Q] to quit, leave empty to continue:")
    if usr_choice == 'Q':
        break