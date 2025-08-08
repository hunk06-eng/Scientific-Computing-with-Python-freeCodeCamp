# I know using recursion is much simpler, but where is the fun in that.
class Sudoko:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        output_str = ""

        output_str += "Your input:\n"
        for row in self.board:
            for element in row:
                if element == 0:
                    output_str += "#"
                else:
                    output_str += str(element)
                output_str += "  "
            output_str += "\n"

        print("Solving your sudoku...\n")
        output_str += "\nResult:\n"
        for row in self.solve():
            for element in row:
                output_str += str(element)
                output_str += "  "
            output_str += "\n"

        return output_str

    def __is_num_valid_for_row(self, row, num, catch_obs=False):
        if not catch_obs:
            for item in self.board[row]:
                if item == num:
                    return False
            return True
        else:
            obstacles = set()
            for col_idx, item in enumerate(self.board[row]):
                if item == num:
                    obstacles.add((row, col_idx))
            if len(obstacles):
                return obstacles
            return True

    def __is_num_valid_for_col(self, col, num, catch_obs=False):
        if catch_obs:
            obstacles = set()
            for row in range(len(self.board)):
                if self.board[row][col] == num:
                    obstacles.add((row, col))
            if len(obstacles):
                return obstacles
            return True
        else:
            for row in range(len(self.board)):
                if self.board[row][col] == num:
                    return False
            return True

    def __is_num_valid_for_box(self, row, col, num, catch_obs=False):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        if not catch_obs:
            for row_no in range(row_start, row_start + 3):
                for col_no in range(col_start, col_start + 3):
                    if self.board[row_no][col_no] == num:
                        return False
            return True
        else:
            obstacles = set()
            for row_no in range(row_start, row_start + 3):
                for col_no in range(col_start, col_start + 3):
                    if self.board[row_no][col_no] == num:
                        obstacles.add((row_no, col_no))
            if len(obstacles):
                return obstacles
            else:
                return True

    def is_num_valid(self, row, col, num, catch_obstacles=False):
        if not catch_obstacles:
            return all([self.__is_num_valid_for_row(row, num, catch_obstacles),
                        self.__is_num_valid_for_col(col, num, catch_obstacles),
                        self.__is_num_valid_for_box(row, col, num, catch_obstacles)])
        else:
            set1 = self.__is_num_valid_for_row(row, num, catch_obstacles)
            set2 = self.__is_num_valid_for_col(col, num, catch_obstacles)
            set3 = self.__is_num_valid_for_box(row, col, num, catch_obstacles)

            return set1 if set1 is not True else set() | set2 if set2 is not True else set() | set3 if set3 is not True else set()

    def solve(self):
        # used to manually adjust rows, columns as needed.
        row, col = (0, 0)

        # this dictionary is very important to prevent _backtrack() from erasing/editing the value of an original user input
        # it is also used to prevent trying the same digit twice when backtracking and filling the erased slot
        empty_slots_and_tried_digits = {
            (row, col): set() for row in range(len(self.board)) for col in range(len(self.board[0])) if self.board[row][col] == 0
        }

        while True: # loop as many times as necessary.
            if (row, col) in empty_slots_and_tried_digits.keys(): # make sure we aren't editing original user input
                for digit in range(1, 10):
                    if self.is_num_valid(row, col, digit, False):
                        self.board[row][col] = digit
                        empty_slots_and_tried_digits[(row, col)].add(digit)
                        break # no need to continue trying other digits, already found a valid solution.

                if self.board[row][col] == 0: # still empty, no valid option found, requesting backtracking.
                    empty_slots_and_tried_digits[(row, col)] = set()
                    row, col = self.__manual_index_handling(row, col, True)
                    row, col = self.__backtrack(row, col, empty_slots_and_tried_digits)
                    continue
                    # the next if statements don't need to execute
                    # the rows and cols returned from __backtrack are ready.

                next_iteration_instructions = self.__manual_index_handling(row, col, False)
                if next_iteration_instructions is False: # (8, 8) cant iterate anymore.
                    return self.board
                else:
                    row, col = next_iteration_instructions
            else:
                next_iteration_instructions = self.__manual_index_handling(row, col, False)
                if next_iteration_instructions is False:
                    return self.board
                else:
                    row, col = next_iteration_instructions

    def __backtrack(self, row, col, tried_digits):
        while True: # backtrack until an alternative solution is found
            if (row, col) in tried_digits.keys(): # make sure were not backtracking over an original slot (user input)
                for digit in range(1, 10):
                    if digit not in tried_digits[(row, col)]: # make sure we are trying a new digit
                        if self.is_num_valid(row, col, digit, False):
                            self.board[row][col] = digit
                            tried_digits[(row, col)].add(digit)

                            next_iteration_instructions = self.__manual_index_handling(row, col, False)
                            if next_iteration_instructions is False: # (8, 8)
                                print('ERROR')
                                exit()
                            else:
                                row, col = next_iteration_instructions
                                return row, col # return row, col for the solve() loop to pickup from
                # if the loop fails to find an alternative solution, continue backtracking
                self.board[row][col] = 0 # erase older solution until backtracking returns True
                tried_digits[(row, col)] = set()

                """
                Explaining important algorithm logic in here
                The main reasons tried_digits or empty_slots_and_tried_digits dictionary exists is:
                1) to prevent editing original user input
                
                # why add digits that passed is_num_valid to empty_slots_and_tried_digits dictionary in the solve func?
                2) to prevent backtrack function from trying entries (that passed is_num_valid) that the solve() method already tried
                # imagine calling backtrack function, only for it to backtrack to another entry and try the same number solve() tried...
                # this would eventually lead to the same dead-end again
                # we want the backtrack function to find a different solution, not the same solution
                
                # why not just use digit != self.board[row][col] in your for loop
                3) because this could lead to an infinite loop where it tries another digit, it leads to a dead end, so it tries the original digit again
                and that also leads to a dead end, the same one it encountered on its first call. But it also makes it impossible to track what backtrack func
                has already tried.
                
                # why add digits that passed is_num_valid to tried_digits dictionary in the backtrack func?
                4) to prevent the backtrack function from trying numbers it had already tried, yet led to another deadend that resulted in it being called again.
                # imagine this:
                solve gets stuck, backtrack iterates back to num 1
                backtrack decides to make num = 3
                solve also encounters a dead end, calls backtrack
                backtrack changes the num to another valid option, such as num = 5
                solve encounters another dead end, calls backtrack again...
                then, backtrack changes the num to a previous valid option, which is 3
                Then same deadend again..
                
                Solve doesn't care, it'll use the same entries it used previously, the first one it finds, which means the same exact dead ends over and over again.
                So, make backtrack pay for solve stupidity, make it remember that these numbers led to dead ends and avoid using them
                
                # why erase the tried_digits values for the current row, col after its zerod? in tried_digits[(row, col)] = set()
                5) because prohibiting these digits from the backtrack function is logically flawed when the entries behind the zerod entry will change..
                when an entry is zerod, that means the backtrack function is preparing to move to the previous entry,
                if any entry before our current one changes, that means the current numbers we prohibited backtrack from using might might not lead to dead ends anymore.
                Why would it not lead to dead ends anymore?
                Because now solve is required to place different numbers, as is_num_valid will behave differently to certain entries
                
                Not same path == not same dead ends == No more infinite loops
                """

                next_iteration_instructions = self.__manual_index_handling(row, col, True)
                if next_iteration_instructions is False: # (0, 0) cant backtrack anymore ):
                    print('ERROR')
                    exit()
                else:
                    row, col = next_iteration_instructions
            else: # iterating over an original input, go back.
                next_iteration_instructions = self.__manual_index_handling(row, col, True)
                if next_iteration_instructions is False: # (0, 0), can't backtrack anymore.
                    print('ERROR')
                    exit()
                else:
                    row, col = next_iteration_instructions

    def __manual_index_handling(self, row, col, backtrack_status):
        if not backtrack_status:
            if col == len(self.board[0]):
                col = 0
                if row == len(self.board):
                    return False # no index handling, already reached limit (8, 8)
                else:
                    row += 1
            else:
                col += 1
            return row, col
        else:
            if col == 0:
                col = len(self.board[0])
                if row == 0:
                    return False # no index handling, already reached limit in backtrack mode (0, 0)
                else:
                    row -= 1
            else:
                col -= 1
            return row, col


sudoku_puzzle = [
    [0, 0, 2, 0, 3, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 3, 1, 0, 2, 0, 0, 0, 0],
    [0, 6, 0, 0, 5, 0, 2, 7, 0],
    [0, 1, 0, 0, 0, 0, 0, 5, 0],
    [2, 0, 4, 0, 6, 0, 0, 3, 1],
    [0, 0, 0, 0, 8, 0, 6, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 1, 3],
    [0, 0, 5, 3, 1, 0, 4, 0, 0]
]

test_case = Sudoko(sudoku_puzzle)
print(test_case)