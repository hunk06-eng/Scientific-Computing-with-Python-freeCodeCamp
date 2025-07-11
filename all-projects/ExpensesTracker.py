"""
This is the same as the freeCodeCamp lambda expense tracker project, but with a clearer syntax, added error handling
Also allowed for expenses to be stored locally to be reused as needed. Added more options. Happy learning :)
"""

def list_expenses(expenses):
    if len(expenses) == 0:
        print("No expenses found!")
        return

    for category in expenses:
        print(f"Category: {category}, Amount: {expenses[category]}")

def show_total(expenses):
    total = 0
    for amount in expenses.values():
        total += sum(amount)

    print("The total amount of expenses is:", total)

def write_to_txt(expenses, choice):
    with open("expenses_log.txt", choice) as txt:
        if len(expenses) == 0:
            print("Text file was created, but no expenses were saved because none existed!")
        else:
            for key in expenses:
                txt.write(f"Category: {key}, Amount: {expenses[key]}\n")
            print("Done! Stored locally on a text folder.")

def scan_duplicates():
    categories = []
    seen = set()
    try:
        with open("expenses_log.txt", "r") as txt:
            for line in txt.readlines():
                line = line[:-1]
                categories.append(line[line.index(":") + 2:line.index(",")])
    except FileNotFoundError:
        print("Cannot scan for duplicates because file does not exist!")
    for category in categories:
        if category in seen:
            return True
        else:
            seen.add(category)
    return False

def clean_duplicates(scanOrder=1):
    if scanOrder:
        if scan_duplicates():
            print("Duplicate categories found, beginning cleaning...")
        else:
            print("No duplicate categories were found! Quitting cleaning...")
            return

    new_expense = {}
    with open("expenses_log.txt", "r") as txt:
        for line in txt.readlines():
            line = line[:-1]
            new_expense[line[line.index(":") + 2:line.index(",")]] = line[line.index("["):line.index("]") + 1]
    with open("expenses_log.txt", "w") as txt:
        for key in new_expense:
            txt.write(f"Category: {key}, Amount: {new_expense[key]}\n")
        print("Done! Removed all duplicates")

def load_from_txt(expenses):
    try:
        with open("expenses_log.txt", "r") as txt:
            for line in txt:
                line = line[:-1]
                expenses[line[line.index(":")+2:line.index(",")]] = line[line.index("["):line.index("]")+1]
    except FileNotFoundError:
        print("Text file doesn't exist, you must create one using choice number [5] before proceeding.")
        return

    # converting value from string to a list of integers
    new_val = []
    keys = list(expenses.keys())
    s = ''

    for count, value in enumerate(expenses.values()):
        for digit in value:
            if digit.isdigit() or digit == '.':
                s += digit
            elif digit == ',' or digit == ']':
                new_val.append(float(s))
                s = ''
        expenses[keys[count]] = new_val
        new_val = []
    print("Successfully loaded expense list from text file!")
if __name__ == "__main__":
    def main():
        expenses = {}
        count = 0
        writing_to_txt = 0

        while True:
            if count % 4 == 0:
                print('\nExpense Tracker')
                print('1. Add an expense')
                print('2. List all expenses')
                print('3. Show total expenses')
                print('4. Filter expenses by category')
                print('5. Save expenses locally, or erase the local version')
                print('6. Use older expenses stored locally')
                print('7. Remove duplicate categories in expenses_log.txt')
                print('8. Scan for duplicate categories in expenses_log.txt without removal')
                print('9. Exit')
            count += 1

            choice = input("\nEnter your choice: ").strip()
            if choice == '1':
                category = input("Enter expense category: ").strip().capitalize()
                try:
                    amount = float(input("Enter cost: ").strip())
                except ValueError:
                    print("You cant only insert digits into amount, no currencies or strings!")
                    continue

                if category in ['[', ']', ',', ':']:
                    print("Category cannot have '[' or ']', comma (,) or colon (:). Please try again.")
                    continue
                elif category in expenses:
                    expenses[category].append(amount)
                else:
                    expenses[category] = []
                    expenses[category].append(amount)

            elif choice == '2':
                list_expenses(expenses)

            elif choice == '3':
                show_total(expenses)

            elif choice == '4':
                category = input("Enter category to filter: ").strip().capitalize()
                if category in expenses:
                    print(expenses[category])
                else:
                    print("Category doesn't exist, please remember that categories are case-sensitive.")
                    continue

            elif choice == '5':
                choice = input("Enter [w] for erasing expenses_log contents and replacing them with this session expenses\nOr enter [a] for saving all expenses of this session (locally) while keeping older entries: ")
                if choice not in ['w', 'a']:
                    print("Please enter a valid option.")
                    continue

                write_to_txt(expenses, choice)
                writing_to_txt += 1

                if writing_to_txt % 3 == 0:
                    if scan_duplicates():
                        print("Warning! Duplicate categories were found in expenses_log, would you like to remove duplicates while keeping most recent entries?")
                        choice = input("Enter [7] for removing duplicates, leave empty to ignore: ")
                        if choice == '7':
                            clean_duplicates(0)
                            continue
                        else:
                            continue

            elif choice == '6':
                load_from_txt(expenses)

            elif choice == '7':
                clean_duplicates()

            elif choice == '8':
                print("Duplicates found!" if scan_duplicates() else "No duplicates were found.")

            elif choice == '9':
                print("Exiting the script...")
                break

            else:
                print("Please enter a valid choice.")
                continue
    main()