"""
ArithmeticFormatter:
Because this is a mandatory certificate project and because my code must pass all of fCC's test-cases,
I didn't add more features/UI or divert from core logic required in function (arithmetic_arranger).

**By default, this freeCodeCamp project requires the following:**
1) Cannot accept more than 5 arithmetic problems
2) Can choose to show answers using second parameter, must be set to False by default
3) Doesn't accept more than 2 operands
4) Doesn't accept negative integers, but allows negative answers
5) Doesn't accept multiplication or division

If any of the requirements above are broken, you must return the exact Error statement in the fCC website,
Any other return types when the requirements above are broken will result in your code not passing their test-cases.
"""

def arithmetic_arranger(problems, show_answers=False):
    if len(problems) > 5:
        return "Error: Too many problems."
    numbers = {}
    operators = {}
    lengths = {}
    answers = None
    if show_answers:
        answers = {}
    # iterate through problems list
    # in this for loop, we filter operators (+,-), numbers (0 to 9) using .isdigit(), and check for errors directly
    # all characters filtered are placed in dictionary, each contain an index (idx), this idx represents each arithmetic problem
    # if I enter 0 into numbers[0]/operators[0]/lengths[0] I will be given all these properties of the first arithmetic problem in problems(list)
    # thus, these dictionaries are ordered by KEY, and each KEY is preserved for a specific arithmetic problem
    for idx, arithmetic in enumerate(problems):
        first_num_placeholder = ""
        second_num_placeholder = ""
        operator = None
        second_num = False
        for string in arithmetic:
            if string.isdigit():
                # second_num is a boolean checking whether we are dealing with the first or second operand
                # second_num resets to false at the start of each new arithmetic problem
                # when the for loop finds an operator (+, -) second_num is set to True
                # ['32 + 1']: when for loop reaches (+) set second_num to True to prepare for adding 1 to second_num_placeholder
                if second_num:
                    second_num_placeholder += string
                else:
                    first_num_placeholder += string
            elif string == "+" or string == "-":
                if second_num:
                    operator = string
                else:
                    return "Error: Negative numbers are not allowed."
            # division or multiplying is not allowed.
            elif string == "/" or string == "*":
                return "Error: Operator must be '+' or '-'."
            else:
                if string == " ":
                    second_num = True
                # spaces are allowed, anything else that didn't pass the above if-statements must be an illegal char
                # like a letter ['31gx' + '5']
                else:
                    return "Error: Numbers must only contain digits."
        if len(first_num_placeholder) > 4:
            return "Error: Numbers cannot be more than four digits."
        if len(second_num_placeholder) > 4:
            return "Error: Numbers cannot be more than four digits."
        # adding results of the current item in problems(list) in the dictionaries we talked about earlier
        # notice how each dictionary has the exact same key
        numbers[idx] = [int(first_num_placeholder), int(second_num_placeholder)]
        operators[idx] = operator
        if show_answers:
            # if user wants to show answers, we must also save arithmetic problem result in answers dictionary
            # if the operation is addition, simply use sum(), if its subtraction, subtract first_num - second_num in order
            answers[idx] = sum(numbers[idx]) if operator == "+" else (int(first_num_placeholder)-int(second_num_placeholder))

        # decide amount of dashes '-' and the total length of the arithmetic problem
        if show_answers:
            # if the user wants to show answers, to find the length of the arithmetic problem
            # we must compare the length of the longest operand to the length of the answer
            # this decides how many dashes we will use
            answer_len = None
            operands_len = max(len(first_num_placeholder), len(second_num_placeholder)) + 2 # + 2 for the space and the operator between the longest operand
            if operators[idx] == "+":
                answer_len = len(str(int(first_num_placeholder) + int(second_num_placeholder)))
            elif operators[idx] == "-":
                answer_len = len(str(int(first_num_placeholder) - int(second_num_placeholder)))
            lengths[idx] = max(operands_len, answer_len) # which is longer? the longest operand or the answer? important for later
        else:
            lengths[idx] = max(len(first_num_placeholder), len(second_num_placeholder)) + 2

    output = ""

    # [key][idx] [0][0] --> [1][0] --> [2][0] etc..
    # idx represents lines
    # key represents each arithmetic problem
    # here, we are printing each line horizontally, not vertically
    # we need 4 lines if user wants to show_answers, 3 lines if no answers are shown.
    for idx in range(4 if show_answers else 3):
        for key in range(len(problems)):
            if idx == 0: # if we are at first line
                # because digits must start from the right in each arithmetic problem
                # we must subtract the total arithmetic problem length by the length of the operand we are currently it
                # this way we can figure out how many spaces are needed
                spaces = lengths[key]-len(str(numbers[key][0]))
                # add spaces first, then add the operand itself. This way the operand is on the right.
                output += " "*spaces if spaces != 0 else "" # the ternary statement is necessary, if spaces was zero, the script will crash
                output += str(numbers[key][0]) # adding the operand to output
                if key != (len(problems)-1): # adding 4 spaces between each arithmetic problem, except the last one, hence the if statement
                    output += "    "
            elif idx == 1: # second line
                output += operators[key] # operator can only be on second line
                # (-1) in spaces because in the second line because operator takes a single space
                spaces = lengths[key]-len(str(numbers[key][1]))-1
                output += " " * spaces if spaces != 0 else ""
                output += str(numbers[key][1])
                if key != (len(problems)-1):
                    output += "    "
            elif idx == 2:
                output += "-"*lengths[key] # adding dashes using the length of each arithmetic problem we calculated previously
                if key != (len(problems)-1):
                    output += "    "
            elif idx == 3: # this elif statement will not run if user chooses to set show_answers to False, because it is for the 4th line
                spaces = lengths[key]-(len(str(answers[key])))
                output += " "*spaces if spaces != 0 else ""
                output += str(answers[key])
                if key != (len(problems)-1):
                    output += "    "
        if idx != (3 if show_answers else 2): # here, before starting a new line (changing the value of idx) we use '\n' to start a new line
            # the if statement above is necessary to avoid executing output += "\n" at the last loop run
            # because in fCC adding lines after the arithmetic problem has ended (like adding a line after the dash "-") would result in output being rejected
            output += "\n"

    return output

# You can uncomment the next line to test this script.
#print(arithmetic_arranger(["3 - 5", "74 - 22", "30 - 90", "100 + 5054", "7123 - 9253"], True))