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


"""
Those are some of freeCodeCamp test-cases, you can remove the docstring to test the code.

print(add_time('3:00 PM', '3:10'),
# Returns: 6:10 PM

add_time('11:30 AM', '2:32', 'Monday'),
# Returns: 2:02 PM, Monday

add_time('11:43 AM', '00:20'),
# Returns: 12:03 PM

add_time('10:10 PM', '3:30'),
# Returns: 1:40 AM (next day)

add_time('11:43 PM', '24:20', 'tueSday'),
# Returns: 12:03 AM, Thursday (2 days later)

add_time('6:30 PM', '205:12'))
# Returns: 7:42 AM (9 days later)
"""