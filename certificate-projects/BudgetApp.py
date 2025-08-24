class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = [] # for each category instance

    def __str__(self):
        str_output = [self._prepare_tite_for_output()]
        if len(self.ledger) == 0:
            return str_output[0]

        for info in self.ledger:
            amount = self._prepare_amount_for_output(info["amount"])
            spaces_in_between = " " * (30 - (len(info["description"][:23]) + len(amount)))
            str_output.append(f"\n{info['description'][:23]}{spaces_in_between}{amount}")

        str_output.append(f"\nTotal: {self._prepare_amount_for_output(self.get_balance())}")
        return "".join(str_output)

    @staticmethod
    def _prepare_amount_for_output(amount):
        is_float = isinstance(amount, float)
        amount = str(amount).split(".")

        if is_float:
            if len(amount[1]) < 2:
                amount[1] += "0"
        else:
            amount.append("00")

        return ".".join(amount)

    def _prepare_tite_for_output(self):
        amount_of_stars = 30-len(self.category) # calculate first line stars
        str_output = ["*" * (amount_of_stars // 2)] # calculate the left side (before category name)

        amount_of_stars -= len(str_output[0]) # remove the added stars on the left side from the total amount of stars
        str_output.append(f"{self.category}") # add the category name in the center
        str_output.append("*"*amount_of_stars) # add the remaining stars

        return "".join(str_output)

    def check_funds(self, amount):
        if self.get_balance() < amount:
            return False
        return True

    def get_balance(self):
        balance = 0
        for dic in self.ledger:
            balance += dic["amount"]
        return balance

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # will be back (for False return cases)
        if not self.check_funds(amount):
            return False # check_funds will return False if not enough funds exist for withdrawal

        self.ledger.append({"amount": -amount, "description": description})
        return True

    def transfer(self, new_category_amount, new_category_instance):
        # withdraw from current category
        if self.withdraw(new_category_amount, f"Transfer to {new_category_instance.category}"):
            # add to new category, only if withdrawal succeeds. (enough funds exist)
            new_category_instance.deposit(new_category_amount, f"Transfer from {self.category}")
            return True # transfer complete
        return False # transfer not complete, not enough funds to withdraw from in current instance.

def create_spend_chart(categories):
    total = 0
    spent_by_category = {instance_name.category: 0 for instance_name in categories}
    percentage_by_category = spent_by_category.copy()

    for category in categories:
        for info in category.ledger:
            num = info["amount"]
            if num < 0:
                num = abs(num)
                spent_by_category[category.category] += num
                total += num

    for category, spent in spent_by_category.items():
        # the percentage of each category, floored to closest 10
        percentage_by_category[category] = int((spent/total) * 100)

    output_str = ["Percentage spent by category"]

    for percentage in range(100, -10, -10): # from 100 to 0, output line by line
        spaces_to_add = " " * (3-len(str(percentage)))
        output_str.append(f"\n{spaces_to_add}{percentage}| ")
        for category, calculated_percentage in percentage_by_category.items():
            if percentage <= calculated_percentage:
                output_str.append("o  ")
            else:
                output_str.append("   ")
    output_str.append("\n    -")
    output_str.append("-"*3*len(categories))

    max_len = 0
    categories_len = {}
    for category in spent_by_category.keys():
        categories_len[category] = len(category)
        if len(category) > max_len:
            max_len = len(category)

    for line in range(max_len):
        output_str.append("\n     ")
        for category in categories_len.keys():
            if line < categories_len[category]:
                output_str.append(f"{category[line]}  ")
            else:
                output_str.append("   ")

    return "".join(output_str)

if __name__ == "__main__":
    def create_category_list():
        categories_name = input("Categories must be seperated by a single comma, in this form: food,car,gym,clothing\nYour categories: ").strip().title().split(",")
        instance_holder = []

        for category_name in categories_name:
            instance_holder.append(Category(category_name))
        return instance_holder

    def show_categories(categories_to_show):
        print("Select a category...")
        for idx, usr_category in enumerate(categories_to_show):
            print(f"({idx + 1}) {usr_category.category}")

    usr_categories = create_category_list()
    while True:
        print("(1) Deposit into a category")
        print("(2) Withdraw from a category")
        print("(3) Transfer C amount of deposits from X category to Y category")
        print("(4) Get financial history for X category")
        print("(5) Create a spending chart")
        print("(6) Flush category list and create a new one")
        print("(7) Show all financial history for ALL categories")
        print("(8) Exit script")

        usr_choice = input("Your choice: ").strip()
        if usr_choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            usr_choice = int(usr_choice)
        else:
            print("Invalid choice, must only input a single digit from 1 to 8")
            continue

        if usr_choice == 1 or usr_choice == 2:
            show_categories(usr_categories)
            req_category = input("Choose your category (by its digit, not name): ").strip()
            if req_category.isnumeric():
                req_category = usr_categories[int(req_category)-1]
                req_amount = input("Enter amount to deposit/withdraw (only digits or floats, only positive): ").strip()
                try:
                    req_amount = float(req_amount)
                except ValueError:
                    print("Error, invalid amount. Can only accept digits or floats: like 53 or 30.54")
                    print("Try again, no spaces, currency signs, commas")
                    continue
                req_description = input("Enter a description to remember the reason for this deposit/withdraw: ")
                if usr_choice == 1:
                    req_category.deposit(req_amount, req_description)
                    print(f"Deposit to {req_category.category} successful.")
                else:
                    if req_category.withdraw(req_amount, req_description):
                        print(f"Withdraw from {req_category.category} successful.")
                    else:
                        print(f"Withdraw from {req_category.category} failed. Not enough funds to withdraw from.")
            else:
                print("Invalid index, you must enter the digit that corresponds to the category")
                print("1 for 1st category, 2 for 2nd category, etc.. No floats or characters.")
                print("Try again.")
                continue

        elif usr_choice == 3:
            show_categories(usr_categories)
            withdraw_from_category = input("Choose your category to transfer from (by its digit, not name): ").strip()
            deposit_to_category = input("Choose your category to transfer to (by its digit, not name): ").strip()

            if withdraw_from_category.isnumeric() and deposit_to_category.isnumeric():
                withdraw_from_category = usr_categories[int(withdraw_from_category)-1]
                deposit_to_category = usr_categories[int(deposit_to_category)-1]

                req_amount = input(f"Enter amount to transfer from {withdraw_from_category.category} to {deposit_to_category.category}: ").strip()
                try:
                    req_amount = float(req_amount)
                except ValueError:
                    print("Error, invalid amount. Can only accept digits or floats: like 53 or 30.54")
                    print("Try again, no spaces, currency signs, commas")
                    continue
                if withdraw_from_category.transfer(req_amount, deposit_to_category):
                    print(f"Successfully transferred {req_amount} from {withdraw_from_category.category} to {deposit_to_category.category}.")
                else:
                    print(f"Failed to transfer {req_amount} from {withdraw_from_category.category} to {deposit_to_category.category}, Not enough funds in {withdraw_from_category.category}.")
            else:
                print("Invalid index, you must enter the digit that corresponds to the category")
                print("1 for 1st category, 2 for 2nd category, etc.. No floats or characters.")
                print("Try again.")
                continue

        elif usr_choice == 4:
            show_categories(usr_categories)
            req_category = input("Choose your category (by its digit, not name): ").strip()
            if req_category.isnumeric():
                req_category = int(req_category)
                print(usr_categories[req_category-1])
            else:
                print("Invalid index, you must enter the digit that corresponds to the category")
                print("1 for 1st category, 2 for 2nd category, etc.. No floats or characters.")
                print("Try again.")
                continue

        elif usr_choice == 5:
            try:
                print(create_spend_chart(usr_categories))
            except ZeroDivisionError:
                print("Cant generate a spending chart because nothing was spent (or withdrawn).")

        elif usr_choice == 6:
            usr_categories = create_category_list()

        elif usr_choice == 7:
            for category_to_output in usr_categories:
                print(category_to_output)

        elif usr_choice == 8:
            print("Exiting script...")
            break

        print("\n")