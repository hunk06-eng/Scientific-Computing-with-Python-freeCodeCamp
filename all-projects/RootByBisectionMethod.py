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

def find_root(number, tolerance=0.0000001, max_iterations=2500):
    # you could also pass tolerance as a complex number, (1e-7)
    if number == 1:
        return 1
    elif number == 0:
        return 0
    elif number < 0:
        raise ValueError("A squared number cannot be negative!")

    root = None
    # if the number is bigger than 1, such as 16, then the root cannot be bigger than 16
    # however if the number is less than 1, such as (1/4), then the root can be bigger than the number itself, in this case sqrt(1/4)=(1/2)
    # to simplify this, if a number is less than 1, its square root cannot be bigger than 1
    start_interval = 0
    end_interval = number if number > 1 else 1

    for i in range(max_iterations):
        mid_interval = (start_interval + end_interval) / 2
        mid_interval_squared = mid_interval ** 2 # square it to check if it is a possible solution

        # if difference between our solution, and the number is within the specified tolerance, return our solution
        if abs(mid_interval_squared - number) <= tolerance:
            root = mid_interval
            return root
        # if it is not, we will have to split the interval more
        # this checks if our solution was bigger than the number itself, if it was, we can discard the mid_interval and whatever is bigger than it.
        elif mid_interval_squared > number:
            # when the next loop runs, a new mid_interval will be calculated.
            end_interval = mid_interval
        elif mid_interval_squared < number:
            # cut whatever is before the mid_interval, since mid_interval squared is less than our number
            # thus, whatever interval we square before mid_interval will also result in a value less than our required number
            start_interval = mid_interval
    if root is None:
        print(f"Couldn't find a root within the specified tolerance")
    else:
        print(f"Couldn't find a root within the specified tolerance, the approximate root is {root}")
    return root

if __name__ == "__main__":
    print("***Root finder using Bisection Method***")
    print("Tolerance refers to the difference between the calculated root (squared), and the number inputted.")
    print("Enter [E] at number prompt to exit.\n")
    while True:
        number_in = input("Enter the number to find the root of: ")
        if number_in == 'E' or number_in == 'e':
            print("Exiting script..")
            break
        tolerance_in = input("Enter [Q] for a quick calculation.\n[D] for a default calculation.\n[P] for a precise calculation.\n[L] for using highest computing power (recommended for highest precision)\nYour Choice: ").strip()

        try:
            number_in = float(number_in)
        except ValueError:
            print("Please enter a valid number! Try again.")
            continue

        if tolerance_in == 'Q' or tolerance_in == 'q':
            tolerance_in = 0.0001
            max_iterations_in = 500
        elif tolerance_in == 'D' or tolerance_in == 'd':
            tolerance_in = 0.0000001
            max_iterations_in = 5000
        elif tolerance_in == 'P' or tolerance_in == 'p':
            tolerance_in = 0.0000000001
            max_iterations_in = 1000000
        elif tolerance_in == 'L' or tolerance_in == 'l':
            tolerance_in = 0.00000000000001
            max_iterations_in = 150000000
        else:
            print("Invalid choice of speed! Try again.")
            continue

        print(f"The root of your number is: {find_root(number_in, tolerance_in, max_iterations_in)}\n")