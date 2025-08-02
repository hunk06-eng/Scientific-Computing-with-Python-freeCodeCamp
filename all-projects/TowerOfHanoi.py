def find_legal_move(the_tower, disk_num, disk_loc, biggest_disk):
    loc = disk_loc[disk_num]

    if disk_num != the_tower[loc][-1]: # if the disk is not the top disk, then it cannot be moved.
        if disk_num < biggest_disk:
            find_legal_move(the_tower, disk_num + 1, disk_loc, biggest_disk)
            return

    look_into = {'source': {'auxiliary', 'target'},
                 'auxiliary': {'source', 'target'},
                 'target': {'source', 'auxiliary'}
                 }


    for tower in look_into[loc]:
        if len(the_tower[tower]) == 0: # no need to check for (disk_num == the_tower[loc][-1]) because we already checked for that above.
            the_tower[loc].remove(disk_num)
            the_tower[tower].append(disk_num)
            disk_loc[disk_num] = tower
            return
        elif len(the_tower[tower]) != 0 and the_tower[tower][-1] > disk_num:
            the_tower[loc].remove(disk_num)
            the_tower[tower].append(disk_num)
            disk_loc[disk_num] = tower
            return

def solve_tower_puzzle(num_of_disks, tower, disk_loc):
    """
    If n is EVEN: The smallest disk cycle is
    Source -> Auxiliary -> Target -> Source
    Then any other legal move, except moving the smallest disk.
    Repeat.

    If n is ODD: The smallest disk cycle is
    Source -> Target -> Auxiliary -> Source
    Then any other legal move, except moving the smallest disk.
    Repeat.

    Every odd move, 1st, 3rd, 5th, etc. the smallest disk is moved.
    """

    num_of_moves = (2**num_of_disks)-1 # (2^n) - 1 is the minimum amount of moves needed to solve the puzzle.
    # if even, follow the even cycle for smallest disk, if odd, follow the odd cycle for smallest disk.
    tower_cycle = ['source', 'auxiliary', 'target'] if num_of_disks % 2 == 0 else ['source', 'target', 'auxiliary']
    cycle_idx = 1

    for move in range(1, num_of_moves+1):
        if move % 2 != 0: # odd move means move small disk.
            # cycle_idx % 3 tells us where the smallest disk is supposed to be.
            # (cycle_idx - 1) % 3 tells us which tower is the smallest disk located on.
            tower[tower_cycle[cycle_idx%3]].append(tower[tower_cycle[(cycle_idx-1)%3]].pop())
            cycle_idx += 1
        else: # if it's an even move, we must make a legal move, but avoid moving the smallest disk. There's only one legal move everytime.
            find_legal_move(tower, 2, disk_loc, num_of_disks)

    return tower

if __name__ == "__main__":
    while True:
        choice = input("Enter [Q] to quit.\nEnter amount of disks in source tower to begin the script: ").strip()
        try:
            if choice.upper() == 'Q':
                print("quitting script...")
                break

            choice = int(choice)
            if choice < 0:
                raise ValueError
        except ValueError:
            print("Invalid integer! Can't be a string or character, can't be less than zero, must be integer only (no floats)")
            print("Please try again...\n")
            continue

        # create the disks, and two empty towers
        hanoi_tower = {
            'source': list(range(choice, 0, -1)),
            'auxiliary': [],
            'target': []
        }

        # used later to keep track of disk locations (for faster access)
        disk_locations = {val: 'source' for val in hanoi_tower['source'] if val != 1}

        print(f"Result: {solve_tower_puzzle(choice, hanoi_tower, disk_locations)}\n")

        stop_or_not = input("Continue? [Y] for yes, [N] for no: ").strip()
        if stop_or_not.upper() == 'N':
            print("quitting script...")
            break