"""
I understand that recursion would be much simpler, and cleaner.
However, I chose to create my own solution instead to force myself to think.
Because the best way to learn is through forcing uniqueness.

A small Q&A that answers questions about core algorithm logic in solve() and _backtrack() methods:

# one of the main uses of tried_digits or empty_slots_and_tried_digits dictionary is:
1) to prevent editing original user input

# why add digits that passed is_num_valid check to empty_slots_and_tried_digits dictionary in solve() func?
2) to prevent backtrack function from trying entries (that passed is_num_valid) that the solve() method already tried
* imagine calling backtrack function, only for it to backtrack to another entry and try the same number solve() tried...
* this would eventually lead to the same dead-end again
* we want the backtrack function to find a different solution, not the same solution

# why add digits that passed is_num_valid to tried_digits dictionary in _backtrack func?
3) to prevent the backtrack function from trying numbers it had already tried, yet led to another deadend that resulted
in it being called again.
* the solve method doesn't care, it'll use the same entries it used previously, the first valid digit it finds
* which means the same exact dead ends over and over again.
* so, make backtrack add an extra check, make it remember that these numbers led to dead ends and avoid using them.
* if this check doesn't exist, the solve method will generate the same exact digits it used before backtracking,
and call backtrack again.

# why erase the tried_digits values for the current row, col after its zerod? tried_digits[(self.row, self.col)] = set()
4) because prohibiting these digits from the backtrack function is logically flawed when the entries behind the
zerod entry will change.
* when an entry is zerod, that means the backtrack function is preparing to move to the previous entry,
* if any entry before our current one changes, that means the current numbers we prohibited backtrack from using might
not lead to dead ends anymore.
# why would it not lead to dead ends anymore?
* because now solve is required to place different numbers, as is_num_valid will behave differently to certain entries
in short: not same path == not same dead ends
"""

class Sudoko:
    def __init__(self, board):
        self.board = [row.copy() for row in board] # do not mutate board directly. create a shallow copy.
        # if solve() is called self.board will be altered, self.board_original will remain untouched.
        # useful when outputting original user input
        self.board_original = board
        # rows, cols are used in methods like in solve(), _backtrack(), _manual_index_handling()
        self.row = 0
        self.col = 0
        self._is_board_structure_valid() # ensure user input is valid, raises errors if sudoku is invalid.
        self.is_solved = False # set to true whenever solve() returns something. Used in __str__


    def __str__(self):
        # check if sudoku was solved.
        output_string = []
        if self.is_solved:
            output_string.append("Your input:\n")
            # start with original board before solving
            for row in self.board_original:
                for item in row:
                    if item == 0:
                        output_string.append("#")
                    else:
                        output_string.append(str(item))
                    output_string.append("  ")
                output_string.append("\n")
            output_string.append("\nYour solved sudoku:\n")

            # then, do the same with the solved board.
            for row in self.board:
                for item in row:
                    output_string.append(str(item))
                    output_string.append("  ")
                output_string.append("\n")

            return "".join(output_string)
        else:
            output_string.append("Note: The sudoku was not solved, because solve() method was never called.\n")

            for row in self.board_original:
                for item in row:
                    if item == 0:
                        output_string.append("#")
                    else:
                        output_string.append(str(item))
                    output_string.append("  ")
                output_string.append("\n")
            return "".join(output_string)

    def _is_board_structure_valid(self):
        # ensure there is 9 rows
        if len(self.board) != 9:
            raise IndexError("Sudoku must have 9 lines (rows). (9x9)")

        # ensure there is 9 columns in each row
        for line in self.board:
            if len(line) != 9:
                raise IndexError("Sudoku must have 9 digits in each line (row). (9x9)")

        # check if number is valid in its row, col, box
        for row in self.board:
            for item in row:
                if item != 0:
                    original_entry = self.board[self.row][self.col]
                    self.board[self.row][self.col] = 0 # temporary to make is_num_valid to function correctly
                    state = self.is_num_valid(original_entry, True)

                    if len(state):
                        raise ValueError(f"Invalid sudoku detected! Number {item}"
                                         f" at row {self.row} and column {self.col} has obstacles"
                                         f" in the following indexes: {state}")
                    else:
                        self.board[self.row][self.col] = original_entry # reset to the original entry
                self.col += 1
            self.row += 1
            self.col = 0
        self.row = 0 # reset row, col to zero for later usage
        self.col = 0
        return True # once everything is over, exit function and return True

    def _is_num_valid_for_row(self, num, catch_obstacles=False):
        if catch_obstacles:
            obstacles = set()
            for col_idx, item in enumerate(self.board[self.row]):
                if item == num:
                    obstacles.add((self.row, col_idx))
            return obstacles
        else:
            for item in self.board[self.row]:
                if item == num:
                    return False
            return True

    def _is_num_valid_for_col(self, num, catch_obstacles=False):
        if catch_obstacles:
            obstacles = set()
            for row in range(len(self.board)):
                if self.board[row][self.col] == num:
                    obstacles.add((row, self.col))
            return obstacles
        else:
            for row in range(len(self.board)):
                if self.board[row][self.col] == num:
                    return False
            return True

    def _is_num_valid_for_box(self, num, catch_obstacles=False):
        row_start = (self.row // 3) * 3
        col_start = (self.col // 3) * 3

        if catch_obstacles:
            obstacles = set()
            for row_no in range(row_start, row_start + 3):
                for col_no in range(col_start, col_start + 3):
                    if self.board[row_no][col_no] == num:
                        obstacles.add((row_no, col_no))
            return obstacles
        else:
            for row_no in range(row_start, row_start + 3):
                for col_no in range(col_start, col_start + 3):
                    if self.board[row_no][col_no] == num:
                        return False
            return True

    def is_num_valid(self, num, catch_obstacles=False):
        is_row_valid = self._is_num_valid_for_row(num, catch_obstacles)
        is_col_valid = self._is_num_valid_for_col(num, catch_obstacles)
        is_box_valid = self._is_num_valid_for_box(num, catch_obstacles)

        return all([is_row_valid, is_col_valid, is_box_valid]) if not catch_obstacles else is_row_valid|is_col_valid|is_box_valid

    def solve(self):
        # this dictionary is very important to prevent _backtrack() from erasing/editing the value of an original user input
        # it is also used to prevent trying the same digit twice when backtracking and filling the erased slot
        empty_slots_and_tried_digits = {
            (row, col): set() for row in range(len(self.board)) for col in range(len(self.board[0])) if self.board[row][col] == 0
        }

        while True: # loop as many times as necessary.
            if (self.row, self.col) in empty_slots_and_tried_digits.keys(): # make sure we aren't editing original user input
                for digit in range(1, 10):
                    if self.is_num_valid(digit, False):
                        self.board[self.row][self.col] = digit
                        empty_slots_and_tried_digits[(self.row, self.col)].add(digit)
                        break # no need to continue trying other digits, already found a valid solution.

                if self.board[self.row][self.col] == 0: # still empty, no valid option found, requesting backtracking.
                    empty_slots_and_tried_digits[(self.row, self.col)] = set()
                    self._manual_index_handling(True)
                    self._backtrack(empty_slots_and_tried_digits)
                    continue
                    # the next if statements don't need to execute
                    # the rows and cols returned from _backtrack are ready.

                if not self._manual_index_handling(False): # (8, 8) cant iterate anymore.
                    self.is_solved = True
                    return self.board
            else:
                if not self._manual_index_handling(False):
                    self.is_solved = True
                    return self.board

    def _backtrack(self, tried_digits):
        while True: # backtrack until an alternative solution is found
            if (self.row, self.col) in tried_digits.keys(): # make sure were not backtracking over an original slot (user input)
                for digit in range(1, 10):
                    if digit not in tried_digits[(self.row, self.col)]: # make sure we are trying a new digit
                        if self.is_num_valid(digit, False):
                            self.board[self.row][self.col] = digit
                            tried_digits[(self.row, self.col)].add(digit)
                            self._manual_index_handling(False) # Call manual index to move forward one index
                            # it is not needed to check if called function (_manual_index_handling) above is false,
                            # because the highest possible value of row, col when _backtrack is called is (8, 7)
                            return True

                # if the loop fails to find an alternative solution, continue backtracking
                self.board[self.row][self.col] = 0 # erase older solution until backtracking returns True
                tried_digits[(self.row, self.col)] = set()

                if not self._manual_index_handling(True): # (0, 0) cant backtrack anymore ):
                    raise ValueError("Backtracking has been fully exhausted, board is unsolvable.")
            else: # iterating over an original input, go back.
                if not self._manual_index_handling(True): # (0, 0), can't backtrack anymore ):
                    raise ValueError("Backtracking has been fully exhausted, board is unsolvable.")

    def _manual_index_handling(self, backtrack_status):
        if not backtrack_status:
            if self.col == len(self.board[0]):
                self.col = 0
                if self.row == len(self.board):
                    return False # no index handling, already reached limit (8, 8)
                else:
                    self.row += 1
                    return True
            else:
                self.col += 1
                return True
        else:
            if self.col == 0:
                self.col = len(self.board[0])
                if self.row == 0:
                    return False # no index handling, already reached limit in backtrack mode (0, 0)
                else:
                    self.row -= 1
                    return True
            else:
                self.col -= 1
                return True

sudoku_puzzle = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 9, 0, 3, 0, 0],
    [1, 7, 0, 8, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 6, 7],
    [0, 6, 1, 0, 5, 0, 9, 3, 0],
    [9, 3, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 2, 0, 5, 6],
    [0, 0, 3, 0, 4, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0]]

test_case = Sudoko(sudoku_puzzle)
test_case.solve()
print(test_case)