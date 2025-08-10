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

# some tests
food = Category("Food")
clothing = Category("Clothing")
entertainment = Category("Entertainment")

food.deposit(1000, "deposit")
food.withdraw(34.25, "date night")
food.withdraw(50.5, "hanging out")
food.deposit(302.5, "monthly salary")
food.transfer(320, clothing)
clothing.withdraw(50.5, "preparing for party")
clothing.withdraw(30.25, "new running shoes")
clothing.withdraw(67.5, "new perfume")
clothing.transfer(100, entertainment)
entertainment.withdraw(20, "movie ticket")
entertainment.withdraw(40, "tourism")
entertainment.withdraw(40, "music concert")
print(food)
print(clothing)
print(entertainment)

print(create_spend_chart([food, clothing, entertainment]))