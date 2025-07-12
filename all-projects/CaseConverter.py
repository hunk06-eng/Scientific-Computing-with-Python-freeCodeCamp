"""
    This script converts strings in formats like PascalCase, camelCase or snake_case into each other.
    These forms are used to name objects and identifiers, you can guess their format from the way they are written.
    All forms mentioned above do not accept spaces, dashes '-', or any special symbols [!, @, #, %]
    isalnum() only allows digits and alphabetic characters, cool built-in function
"""
def convert_string_to_snake(string_to_convert):
    # cleaning the string from illegal characters
    clean_string = ""
    previous_underscore = False
    for char in string_to_convert:
        if char == '_':
            if not previous_underscore:
                clean_string += "_"
                previous_underscore = True
        elif char.isalnum():
            if char.isupper():
                if not previous_underscore:
                    clean_string += "_" + char.lower()
                else:
                    clean_string += char.lower()
            else:
                clean_string += char

            previous_underscore = False

    return clean_string.lstrip("_")

def convert_string_to_camel(string_to_convert):
    # cleaning the string from illegal characters
    clean_string = ""
    make_upper = False

    for char in string_to_convert:
        if char == '_':
            make_upper = True
        elif make_upper:
            if char.isalnum():
                clean_string += char.upper()
                # only stop using the .upper() method after checking that you are currently iterating through a letter, not a digit
                # this is important to ensure cases like html_5_parser convert correctly to html5Parser
                if not char.isdigit():
                    make_upper = False
        elif char.isalnum():
            clean_string += char

    return clean_string[0].lower() + clean_string[1:]

def convert_string_to_pascal(string_to_convert):
    clean_string = ""
    make_upper = True

    for char in string_to_convert:
        if char == '_':
            make_upper = True
        elif make_upper:
            if char.isalnum():
                clean_string += char.upper()
                # only stop using the .upper() method after checking that you are currently iterating through a letter, not a digit
                # this is important to ensure cases like html_5_parser convert correctly to html5Parser
                if not char.isdigit():
                    make_upper = False
        elif char.isalnum():
            clean_string += char

    return clean_string



if __name__ == "__main__":
    def main():
        print("***\nEnter [Q] at choice prompt to quit the script.\n***")
        print("Warning! String input must be valid in any case (PascalCase, camelCase, snake_case) before input.")
        while True:
            string_to_convert = input("\nEnter string to convert: ")
            choice = input("Enter the case you want to convert to; [P] for PascalCase, [C] for camelCase, [S] for snake_case.\nYour Choice: ").strip()
            # Error handling
            if len(string_to_convert) == 0:
                print("Empty string detected! Restarting loop...")
                continue
            elif string_to_convert == 'Q' or string_to_convert == 'q':
                print("Exiting the script...")
                break
            elif string_to_convert[0].isdigit():
                print("Error, cases cannot start with a digit!")
                print("Most programming languages forbid starting a variable or a function name with a digit.")
                continue
            if choice not in ['P', 'C', 'S', 'p', 'c', 's']:
                print("Invalid choice! Please try again.")
                continue
            else:
                choice = choice.upper()
                if choice == 'S':
                    print(f"Your snake_case string: {convert_string_to_snake(string_to_convert)}")
                elif choice == 'C':
                    print(f"Your camelCase string: {convert_string_to_camel(string_to_convert)}")
                else:
                    print(f"Your PascalCase string: {convert_string_to_pascal(string_to_convert)}")
    main()