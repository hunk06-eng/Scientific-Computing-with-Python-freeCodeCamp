"""
The bisection method is like binary search, it runs multiple times and tries multiple numbers until it finds the closest root
For example: if we use the bisection method to find the root of 16:
1) 16 will be divided by 2, which will give us 8
2) the algorithm will then multiply 8 by itself, 8*8 = 64
3) because 64 is bigger than 16, we can discard 8 and any number that's after it (9*9=81, 10*10=100, all are bigger than 16)
4) now, our possible solutions are between 0 and 8
5) divide 8 by 2, then try 4*4
6) 4*4 = 16 --> correct WOW
7) check if the difference between the middle of our interval and the actual number is acceptable
8) the most widely used tolerance (difference) is 10^-6 or 10^-7, or 0.000001
9) congrats, you found the root of 16!
"""

def find_root(number, tolerance=1e-7, max_iterations=2e4):
    # you could also pass tolerance as a complex number, (1e-7)
    if number == 1:
        return 1
    elif number == 0:
        return 0
    elif number < 0:
        raise ValueError("A squared number cannot be negative!")

    # if the number is bigger than 1, such as 16, then the root cannot be bigger than 16
    # however if the number is less than 1, such as (1/4), then the root can be bigger than the number itself, in this case sqrt(1/4)=(1/2)
    # to simplify this, if a number is less than 1, its square root cannot be bigger than 1
    start_interval = 0
    end_interval = number if number > 1 else 1
    # need to define the next two variables here so we can use them later outside the for loop scope
    mid_interval = None # mid_interval represents potential roots
    mid_interval_squared = None

    for i in range(int(max_iterations)):
        mid_interval = (start_interval + end_interval) / 2
        mid_interval_squared = mid_interval ** 2.0 # square it to check if it is a possible solution

        # if difference between our solution, and the number is within the specified tolerance, return our solution
        if abs(mid_interval_squared - number) <= tolerance:
            return mid_interval
        # if it is not, we will have to split the interval more
        # this checks if our solution was bigger than the number itself, if it was, we can discard whatever is bigger than mid_interval.
        elif mid_interval_squared > number:
            # our interval now ends at the middle, deleting whatever is bigger than mid_interval
            # when the next loop runs, a new mid_interval will be calculated.
            end_interval = mid_interval
        elif mid_interval_squared < number:
            # cut whatever is before the mid_interval, since mid_interval squared is less than our number
            # thus, whatever interval we square before mid_interval will also result in a value less than our required number
            # our new interval now starts at the middle
            start_interval = mid_interval
    # if the code reaches this line, it means the for loop failed to calculate a root within the specified tolerance
    # we must use the final mid_interval value (possible root value) and return it to user
    # but the difference between mid_interval (squared) and the original number must be less than 1% in order to consider it an approx. value
    if abs(mid_interval_squared - number) <= (number*0.01):
        print(f"Couldn't find a root value within specified tolerance, approximate root is: {mid_interval}")
        return mid_interval
    else:
        print(f"Couldn't find a root within the specified tolerance")
    return mid_interval # return None

if __name__ == "__main__":
    print("***Root finder using Bisection Method***")
    print("Tolerance refers to the difference between the calculated root (squared), and the number inputted.")
    print("Enter [E] at number prompt to exit.\n")
    while True:
        number_in = input("Enter the number to find the root of: ").strip()
        if number_in == 'E' or number_in == 'e':
            print("Exiting script..")
            break
        try:
            number_in = float(number_in)
        except ValueError:
                print("Please enter a valid number! Try again.")
                continue

        tolerance_in = input("---Choices---\n[Q] for a quick calculation.\n[D] for a default calculation.\n[P] for a precise calculation.\n[X] for an extensive calculation.\n[L] for a large number calculation (must be used for 7 significant digits or more, ignores precision)\nYour Choice: ").strip()

        # range() is a lazy function, meaning that it generates numbers on demand, so you can enter large max_iteration numbers without worrying about unused memory size.
        if tolerance_in == 'Q' or tolerance_in == 'q':
            tolerance_in = 1e-2
            max_iterations_in = 1e3 #1k
        elif tolerance_in == 'D' or tolerance_in == 'd':
            tolerance_in = 1e-6
            max_iterations_in = 5e4 #50k
        elif tolerance_in == 'P' or tolerance_in == 'p':
            if len(str(number_in)) > 8:
                print("Warning! Due to the nature of float(), python cannot hold more than 15 significant digits without rounding the rest! Don't expect full precision with the current number.")
            tolerance_in = 1e-8
            max_iterations_in = 1e8 #100m
        elif tolerance_in == 'X' or tolerance_in == 'x':
            # a cool mode, with a tolerance very small, 1*10^(-10) and with a maximum of 500 million iterations.
            # very precise for numbers with a smaller amount of digits
            if len(str(number_in)) > 8:
                print("Warning! Due to the nature of float(), python cannot hold more than 15 significant digits without rounding the rest! Don't expect full precision with the current number.")
            tolerance_in = 1e-10
            max_iterations_in = 5e8 #500m
        elif tolerance_in == 'L' or tolerance_in == 'l':
            if len(str(int(number_in))) < 15:
                tolerance_in = 1e-3
                max_iterations_in = 1e9 #1b
            else:
                tolerance_in = 1e-2
                max_iterations_in = 1e9 #1b
        else:
            print("Invalid choice of speed! Try again.")
            continue

        print(f"The root of your number is: {find_root(number_in, tolerance_in, max_iterations_in)}\n")