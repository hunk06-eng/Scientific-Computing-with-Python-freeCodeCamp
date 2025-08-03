# This is a classical algorithm, so there aren't any touches I can add.
def merge_sort(array):
    # If the length of the array is 1, then it cannot be split anymore (1//2 will return zero), so stop recursion
    if len(array) == 1:
        return None

    # calculate mid-point (for odd lengths: rounded to the biggest integer that is smaller than the float itself, e.g. 7/2 = 3.5 -- > 3)
    mid_point = len(array) // 2
    left_side = array[:mid_point]
    right_side = array[mid_point:]

    # the function will keep calling itself recursively until the array can't be split anymore
    # the left side is always split and fully sorted first
    merge_sort(left_side)
    merge_sort(right_side)

    left_idx, right_idx, arr_idx = 0, 0, 0

    # in recursive calls, the following piece of code first run begins when the actual array is only 2 elements long
    while left_idx < len(left_side) and right_idx < len(right_side):
        if left_side[left_idx] < right_side[right_idx]:
            array[arr_idx] = left_side[left_idx]
            left_idx += 1
            arr_idx += 1
        else:
            array[arr_idx] = right_side[right_idx]
            right_idx += 1
            arr_idx += 1

    # this executes when one side is longer than the other
    # because any left_side or right_side array that have reached this line must be sorted, it is safe to simply add the remaining elements to the array
    if left_idx < len(left_side):
        for _ in range(len(left_side) - left_idx):
            array[arr_idx] = left_side[left_idx]
            left_idx += 1
            arr_idx += 1
    elif right_idx < len(right_side):
        for _ in range(len(right_side) - right_idx):
            array[arr_idx] = right_side[right_idx]
            right_idx += 1
            arr_idx += 1

    return array

def test_cases():
    even_array = [3, 7, 8, 5, 4, 2, 6, 1, 9, 10, 15, 14, 5.5, -2]
    odd_array = [2, 1, 4, 5, -3, -2.4, 0.3, 5.5, 9, 11, 3, 9, 13]
    simple_array = [3, 2, 4, 1, 5, 6]

    even = merge_sort(even_array)
    odd = merge_sort(odd_array)
    simple = merge_sort(simple_array)

    print("Even array results: ", even)
    print("Odd array results: ", odd)
    print("Simple array results ", simple)
    even_array.sort(), odd_array.sort(), simple_array.sort()
    if even == even_array and odd == odd_array and simple == simple_array:
        return True
    else:
        return False

if __name__ == "__main__":
    while True:
        usr_array = []
        how_many = input("Enter amount of numbers in array: ")
        try:
            how_many = int(how_many)
        except ValueError:
            print("Integers only!")
            continue

        for order in range(1, how_many+1):
            if order <= 3:
                if order == 1:
                    choice = input("Enter 1st number: ")
                elif order == 2:
                    choice = input("Enter 2nd number: ")
                else:
                    choice = input("Enter 3rd number: ")
            else:
                choice = input(f"Enter {order}th number: ")
            try:
                choice = float(choice)
            except ValueError:
                print("Invalid float!")
                break
            usr_array.append(choice)
        if len(usr_array) != how_many:
            print("Invalid float entered, please try again...")
            continue

        result = merge_sort(usr_array)
        print("Results: ", result)

        while True:
            exit_or_continue = input("Enter:\n[Q] to quit\n[R] to resume\n[C] to check the previous result\n[T] to run test-cases: ").strip().upper()
            if exit_or_continue == 'Q':
                print("Exiting script")
                exit()
            elif exit_or_continue == 'R':
                break
            elif exit_or_continue == 'C':
                usr_array.sort()
                if result == usr_array:
                    print("Result is correct!")
                else:
                    print("Result is incorrect, something went wrong.")
            elif exit_or_continue == 'T':
                print("Running test-cases")
                if test_cases():
                    print("All test-cases passed")
                else:
                    print("Some/All test-cases failed")
        print("\n")