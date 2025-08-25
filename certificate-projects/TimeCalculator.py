# certificate project

def add_time(start, duration, day=None):
    # each key is the index
    days_in_week = {"Sunday" : 0, "Monday" : 1, "Tuesday" : 2, "Wednesday" : 3, "Thursday" : 4, "Friday" : 5, "Saturday" : 6}
    days_in_week_idx = {0 : "Sunday", 1 : "Monday", 2 : "Tuesday", 3 : "Wednesday", 4 : "Thursday", 5 : "Friday", 6 : "Saturday"}

    # prepare start
    am_or_pm = start[-2:] # AM or PM
    start = start[:-2].rstrip().split(":") # [HH, MM]
    start[0] = int(start[0])
    start[1] = int(start[1])

    # prepare duration
    duration = duration.split(":") # [HH, MM]
    duration[0] = int(duration[0])
    duration[1] = int(duration[1])

    # calculate the amount of days passed from added hours
    days_to_add = duration[0] // 24
    # remove the amount of added days from the duration
    duration[0] -= days_to_add * 24

    # add hours
    while duration[0]:
        to_reach_twelve = 12-start[0]
        if to_reach_twelve:
            if (duration[0]-to_reach_twelve) > 0: # check if duration has enough values to make start[0] reach 12
                am_or_pm = "AM" if am_or_pm == "PM" else "PM"
                if am_or_pm == "AM": # if it becomes AM, that means it was PM, going from PM to AM past 12 means a new day
                    days_to_add += 1
                start[0] += to_reach_twelve
                if start[0] > 12:
                    start[0] %= 12 # remove unnecessary hours
                duration[0] -= to_reach_twelve # remove hours added from duration

            else: # if duration[0] cannot make start[0] reach 12, simply add the remaining amount of the duration without changing AM/PM
                start[0] += duration[0]
                break
        else: # this means that start[0] itself is equal to 12, so simply add 11 hours and let the next iteration do its thing
            start[0] += 11
            start[0] %= 12 # remove unnecessary hours
            duration[0] -= 11

    # add minutes
    while True:
        to_add_hour = 60-start[1]
        # check if duration[1] has enough minutes to add an hour
        if (duration[1] - to_add_hour) >= 0:
            duration[1] -= to_add_hour
            start[0] += 1
            if start[0] >= 12:
                am_or_pm = "AM" if am_or_pm == "PM" else "PM"
                if am_or_pm == "AM": # same as before, if it becomes AM, that means it was PM, going from PM to AM past 12 means a new day
                    days_to_add += 1
                if start[0] > 12:
                    start[0] %= 12
            start[1] = 0 # all minutes consumed for an added hour

        else: # duration[1] cannot add any more hours, simply add minutes directly
            start[1] += duration[1]
            break # break, no need to check if start[1] is bigger than 59, if it was, the upper if statement would execute

    # finally, generate output
    if len(str(start[1])) == 1: # fix cases where output is 9:3PM instead of 9:03PM
        start[1] = "0" + str(start[1])

    if day is None:
        if not days_to_add:
            return f"{start[0]}:{start[1]} {am_or_pm}"
        elif days_to_add == 1:
            return f"{start[0]}:{start[1]} {am_or_pm} (next day)"
        else:
            return f"{start[0]}:{start[1]} {am_or_pm} ({days_to_add} days later)"
    else:
        new_day =  (days_to_add + days_in_week[day.capitalize()]) % 7
        if not days_to_add:
            return f"{start[0]}:{start[1]} {am_or_pm}, {day.capitalize()}"
        elif days_to_add == 1:
            return f"{start[0]}:{start[1]} {am_or_pm}, {days_in_week_idx[new_day]} (next day)"
        else:
            return f"{start[0]}:{start[1]} {am_or_pm}, {days_in_week_idx[new_day]} ({days_to_add} days later)"

def test_cases():
    starting_times = ["3:00 PM", "11:30 AM", "11:43 AM", "10:10 PM", "11:43 PM", "6:30 PM"]
    starting_days = [None, "Monday", None, None, "Tuesday", None]
    times_added = ["3:10", "2:32", "00:20", "3:30", "24:20", "205:12"]
    expected_output = ["6:10 PM", "2:02 PM, Monday", "12:03 PM", "1:40 AM (next day)", "12:03 AM, Thursday (2 days later)", "7:42 AM (9 days later)"]

    test_idx = 0
    for _ in range(len(times_added)):
        print("\n")
        print(f"Start at {starting_times[test_idx]} and add {times_added[test_idx]}", "" if starting_days[test_idx] is None else f"On {starting_days[test_idx]}.")
        result = add_time(starting_times[test_idx], times_added[test_idx], starting_days[test_idx])
        if result == expected_output[test_idx]:
            print(f"Test case number {test_idx+1} passed successfully!")
            print(result)
        else:
            print(f"Test case number {test_idx+1} failed.\nExpected output: {expected_output[test_idx]}\nActual output: {result}")
        test_idx += 1

    if test_idx == len(times_added):
        print("All test-cases passed!")
    else:
        print(f"{len(times_added)-test_idx} test cases failed to pass.")

    print("\n")

if __name__ == "__main__":
    print("--- Time calculator script ---")
    days_of_the_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    while True:
        print("(1) to add time")
        print("(2) to run built-in test cases")
        print("(3) to exit script")

        choice = input("Enter your choice: ").strip()
        if choice not in ["1", "2", "3"]:
            print("Invalid choice, you can only enter a digit from 1 to 3")
            continue

        if choice == "1":
            start_time = input("Enter starting time (before addition) in 12-hour clock format HH:MM AM (leave space before AM/PM).\ne.g. ( 6:30 PM or 11:42 AM ): ").strip()
            start_day = input("Enter the day of the week the starting time was in (Saturday, Monday, Thursday)\n(optional, leave empty if not specified): ").strip().capitalize()
            time_added = input("Enter the time you would like to add to the starting time, in the format (HH:MM), e.g. ( 243:32 ) will add 243 hours and 32 minutes: ").strip()

            if len(start_day):
                if start_day not in days_of_the_week:
                    print(f"Error! {start_day} doesn't exist in {days_of_the_week}. Perhaps you've made a typo?")
                    print("Please try again...")
                    continue
                print(f"The time after adding {time_added} to {start_time} is: {add_time(start_time, time_added, start_day)}")
                continue
            else:
                print(f"The time after adding {time_added} to {start_time} is: {add_time(start_time, time_added)}")
        elif choice == "2":
            test_cases()
            continue
        elif choice == "3":
            print("Exiting script...")
            exit()