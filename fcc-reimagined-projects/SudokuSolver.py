class Sudoku:
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
                        raise ValueError(f"Invalid sudoku detected! Digit {item}"
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
        """
        # one of the main uses of tried_digits or empty_slots_and_tried_digits dictionary is:
        1) to prevent editing original user input

        # why add digits that passed is_num_valid check to empty_slots_and_tried_digits dictionary in solve() func?
        2) to prevent backtrack function from trying entries (that passed is_num_valid) that the solve() method already tried
        * imagine calling backtrack function, only for it to backtrack to another entry and try the same number solve() tried...
        * this would eventually lead to the same dead-end again
        * we want the backtrack function to find a different solution, not the same solution
        """
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
        """
        Quick Q&A
        # why add digits that passed is_num_valid check to the tried_digits dictionary in the _backtrack func?
        1) to prevent the backtrack function from trying numbers it had already tried, yet led to another deadend that resulted
        in it being called again.
        * the solve method doesn't care, it'll use the same entries it used previously, the first valid digit it finds
        * which means the same exact dead ends over and over again.
        * so, make backtrack add an extra check, make it remember that these numbers led to dead ends and avoid using them.
        * if this check doesn't exist, the solve method will generate the same exact digits it used before backtracking,
        and call backtrack again. It'll be stuck in an infinite loop.

        # why erase the tried_digits values for the current row, col after its value is set to zero? in tried_digits[(self.row, self.col)] = set()
        2) because prohibiting these digits from the backtrack function is logically flawed when the entries behind the
        zerod entry will change.
        * when an entry is zerod, that means the backtrack function is preparing to move to the previous entry,
        * if any entry before our current one changes, that means the current numbers we prohibited backtrack from using might
        not lead to dead ends anymore.
        # why would it not lead to dead ends anymore?
        * because now the solve function is required to place different numbers, as is_num_valid will behave differently to certain entries
        * simply put it, the previous entries will change, making it possible to use them in later entries without leading to similar dead ends.
        in short: not same path == not same dead ends
        """
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

def test_cases():
    print("These are computationally demanding sudoku puzzles, please give it a few minutes...")

    # these puzzles were taken from https://github.com/grantm/sudoku-exchange-puzzle-bank
    # each puzzle below was in the diabolical.txt file, with a difficulty rating of 8/10 or more.
    sudoku_test_puzzles = [
        # puzzle 1
        [[0, 7, 0, 6, 0, 4, 0, 2, 0], [0, 0, 0, 3, 0, 8, 0, 0, 0], [0, 0, 6, 0, 5, 0, 4, 0, 0],
         [0, 0, 0, 7, 6, 9, 0, 0, 0], [0, 0, 5, 0, 0, 0, 7, 0, 0], [0, 9, 0, 0, 0, 0, 0, 4, 0],
         [6, 5, 0, 0, 0, 0, 0, 8, 9], [4, 0, 7, 0, 0, 0, 6, 0, 1], [0, 3, 0, 5, 0, 6, 0, 7, 0]],
        # puzzle 2
        [[1, 0, 0, 4, 0, 0, 7, 0, 0], [0, 5, 0, 0, 0, 9, 0, 1, 0], [0, 0, 4, 0, 3, 0, 0, 0, 8],
         [0, 0, 0, 0, 0, 5, 1, 0, 7], [0, 6, 0, 0, 0, 0, 0, 2, 0], [9, 0, 1, 2, 0, 0, 0, 0, 0],
         [2, 0, 0, 0, 6, 0, 8, 0, 0], [0, 3, 0, 5, 0, 0, 0, 4, 0], [0, 0, 6, 0, 0, 4, 0, 0, 9]],
        # puzzle 3
        [[0, 0, 6, 4, 0, 1, 5, 0, 0], [3, 0, 0, 5, 0, 9, 0, 0, 1], [0, 0, 0, 0, 3, 0, 0, 0, 0],
         [2, 0, 5, 0, 0, 0, 7, 0, 3], [0, 3, 0, 0, 4, 0, 0, 2, 0], [6, 7, 0, 0, 0, 0, 0, 5, 8],
         [0, 6, 0, 9, 0, 7, 0, 8, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 2, 3, 0, 4, 9, 0, 0]],
        # puzzle 4
        [[0, 0, 0, 9, 0, 0, 0, 1, 0], [1, 0, 0, 0, 8, 0, 7, 0, 0], [0, 4, 7, 0, 0, 1, 8, 0, 0],
         [0, 0, 8, 0, 4, 0, 0, 0, 1], [0, 6, 0, 3, 0, 8, 0, 4, 0], [4, 0, 0, 0, 6, 0, 5, 0, 0],
         [0, 0, 5, 1, 0, 0, 4, 2, 0], [0, 0, 1, 0, 2, 0, 0, 0, 9], [0, 9, 0, 0, 0, 3, 0, 0, 0]],
        # puzzle 5
        [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 6, 0, 0, 2, 0], [0, 0, 0, 1, 7, 4, 0, 0, 0],
         [3, 0, 0, 7, 0, 5, 0, 0, 6], [0, 4, 0, 0, 3, 0, 0, 5, 0], [0, 0, 5, 2, 0, 1, 8, 0, 0],
         [9, 6, 0, 0, 0, 0, 0, 8, 5], [0, 3, 0, 0, 5, 0, 0, 7, 0], [0, 0, 2, 0, 0, 0, 9, 0, 0]],
        # puzzle 6
        [[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 5, 6, 0, 7, 2, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 3, 5, 0, 6, 1, 0, 0], [9, 0, 0, 0, 4, 0, 0, 0, 7],
         [0, 6, 0, 0, 0, 0, 0, 1, 0], [0, 0, 2, 3, 0, 4, 9, 0, 0], [0, 9, 0, 1, 2, 8, 0, 3, 0]]
    ]

    expected_test_results = [
        # puzzle 1
        [[5, 7, 3, 6, 9, 4, 1, 2, 8], [2, 1, 4, 3, 7, 8, 9, 6, 5], [9, 8, 6, 2, 5, 1, 4, 3, 7],
         [3, 4, 8, 7, 6, 9, 5, 1, 2], [1, 6, 5, 8, 4, 2, 7, 9, 3], [7, 9, 2, 1, 3, 5, 8, 4, 6],
         [6, 5, 1, 4, 2, 7, 3, 8, 9], [4, 2, 7, 9, 8, 3, 6, 5, 1], [8, 3, 9, 5, 1, 6, 2, 7, 4]],
        # puzzle 2
        [[1, 9, 8, 4, 5, 6, 7, 3, 2], [3, 5, 2, 7, 8, 9, 4, 1, 6], [6, 7, 4, 1, 3, 2, 5, 9, 8],
         [4, 2, 3, 6, 9, 5, 1, 8, 7], [5, 6, 7, 8, 1, 3, 9, 2, 4], [9, 8, 1, 2, 4, 7, 3, 6, 5],
         [2, 4, 5, 9, 6, 1, 8, 7, 3], [7, 3, 9, 5, 2, 8, 6, 4, 1], [8, 1, 6, 3, 7, 4, 2, 5, 9]],
        # puzzle 3
        [[9, 8, 6, 4, 7, 1, 5, 3, 2], [3, 4, 7, 5, 2, 9, 8, 6, 1], [5, 2, 1, 8, 3, 6, 4, 9, 7],
         [2, 9, 5, 1, 6, 8, 7, 4, 3], [1, 3, 8, 7, 4, 5, 6, 2, 9], [6, 7, 4, 2, 9, 3, 1, 5, 8],
         [4, 6, 3, 9, 1, 7, 2, 8, 5], [8, 1, 9, 6, 5, 2, 3, 7, 4], [7, 5, 2, 3, 8, 4, 9, 1, 6]],
        # puzzle 4
        [[8, 5, 6, 9, 3, 7, 2, 1, 4], [1, 2, 9, 6, 8, 4, 7, 5, 3], [3, 4, 7, 2, 5, 1, 8, 9, 6],
         [9, 7, 8, 5, 4, 2, 6, 3, 1], [5, 6, 2, 3, 1, 8, 9, 4, 7], [4, 1, 3, 7, 6, 9, 5, 8, 2],
         [7, 3, 5, 1, 9, 6, 4, 2, 8], [6, 8, 1, 4, 2, 5, 3, 7, 9], [2, 9, 4, 8, 7, 3, 1, 6, 5]],
        # puzzle 5
        [[1, 8, 6, 5, 2, 9, 7, 4, 3], [4, 7, 9, 8, 6, 3, 5, 2, 1], [2, 5, 3, 1, 7, 4, 6, 9, 8],
         [3, 2, 8, 7, 9, 5, 4, 1, 6], [7, 4, 1, 6, 3, 8, 2, 5, 9], [6, 9, 5, 2, 4, 1, 8, 3, 7],
         [9, 6, 7, 4, 1, 2, 3, 8, 5], [8, 3, 4, 9, 5, 6, 1, 7, 2], [5, 1, 2, 3, 8, 7, 9, 6, 4]],
        # puzzle 6
        [[6, 2, 4, 8, 1, 5, 7, 9, 3], [8, 3, 5, 6, 9, 7, 2, 4, 1], [7, 1, 9, 4, 3, 2, 8, 5, 6],
         [5, 7, 6, 9, 8, 1, 3, 2, 4], [2, 4, 3, 5, 7, 6, 1, 8, 9], [9, 8, 1, 2, 4, 3, 5, 6, 7],
         [3, 6, 8, 7, 5, 9, 4, 1, 2], [1, 5, 2, 3, 6, 4, 9, 7, 8], [4, 9, 7, 1, 2, 8, 6, 3, 5]]
    ]

    errors_encountered = 0
    for puzzle_number, puzzle in enumerate(sudoku_test_puzzles):
        print(f"Running puzzle number: {puzzle_number+1}")
        try:
            test_result = Sudoku(puzzle)
            result = test_result.solve()
        except ValueError as tst_error:
            print(f"Failure in puzzle number {puzzle_number+1}! Error: {tst_error}")
            errors_encountered += 1
            continue

        if result == expected_test_results[puzzle_number]:
            print(test_result)
            print(f"Puzzle number {puzzle_number+1} passed!")
        else:
            print(f"Failure in puzzle number {puzzle_number+1}! Error: Incorrect Result")
            errors_encountered += 1

    if errors_encountered == 0:
        print("No errors found! All test cases passed!")
        return True
    else:
        print(f"{errors_encountered} errors found of {len(sudoku_test_puzzles)} puzzles.")
        return False

if __name__ == "__main__":
    print("A sudoku puzzle is a 9x9 grid, where we must place digits from 1-9 and ensure the same digit doesn't repeat twice in their column/row/box\n")
    while True:
        print("Enter any of the following choices:")
        print("[1] to solve a sudoku board")
        print("[2] validate a sudoku (e.g. ensure the same digit doesn't repeat twice in its row/column/box)")
        print("[3] to run built-in testcases")
        print("[4] to exit the script\n")

        choice = input("Your choice is: ").strip()
        if choice in ['1', '2', '3', '4']:
            choice = int(choice)
        else:
            print("Invalid value! you must input a single digit [1 to 4] only. (no spaces, commas, dots)")
            print("Please try again...")
            continue

        print("\n")
        if choice == 1 or choice == 2:
            print("Please enter the sudoku you would like to solve/validate line by line (column by column)")
            print("Represent empty cells using a zero (0), and enter digits right next to each other without spaces or commas")
            try:
                usr_sudoku = [[] for _ in range(9)]
                for usr_line in range(9):
                    usr_row = input(f"Enter digits in line number {usr_line+1}: ")
                    if len(usr_row) != 9:
                        raise ValueError("Invalid line! must be 9 digits long only, without anything in between digits. Place a 0 for empty cells.\nExample: 120803005")
                    else:
                        for usr_digit in usr_row:
                            if usr_digit.isnumeric():
                                usr_sudoku[usr_line].append(int(usr_digit))
                            else:
                                raise ValueError(f"You have entered {usr_digit} which is not an integer! not a valid digit.")
                sudoku_instance = Sudoku(usr_sudoku)
                # validation occurs automatically at __init__
                # if incorrect structure, a value error will be raised from the class instance
            except ValueError as error:
                print(f"Error: {error}")
                continue

            if choice == 1:
                sudoku_instance.solve()
                print(sudoku_instance)
            else: # choice == 2
                print("Your sudoku is valid in structure, as no errors were raised.")
            continue

        elif choice == 3:
            if test_cases():
                print("test cases passed!")
            else:
                print("some/all test cases failed to pass ):")
            continue
        else:
            print("Exiting script...")
            break