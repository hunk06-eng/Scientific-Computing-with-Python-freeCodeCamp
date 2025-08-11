# My personal implementations
#### Each script in `fcc-reimagined-projects/` was written from scratch by me, the design, the algorithms and choice of data-structures were selected not for convenience but to maximize learning.

# 💰 Expenses Tracker  
`fcc-reimagined-projects/ExpensesTracker.py`

**Unique Approach**: Interactive CLI with persistent local storage and duplicate management  
- **Challenge**: Track, filter, and sum categorized expenses with robust error handling  
- **Innovation**: Local file storage, duplicate detection/cleaning, and dynamic session management  
- **Key Features**:  
  - Add, list, and filter expenses by category  
  - Save/load expenses to/from a local text file  
  - Detect and remove duplicate categories  
  - Comprehensive input validation and user prompts

# 🧩 Sudoku Solver  
`fcc-reimagined-projects/SudokuSolver.py`

**Unique Approach**: Manual index tracking and iterative backtracking without recursion  
- **Challenge**: Solve Sudoku puzzles while preserving original input and avoiding redundant attempts  
- **Innovation**: Custom dictionaries to track tried digits and prevent repeated dead ends  
- **Key Features**:  
  - Iterative backtracking with manual row/column management  
  - Original board preservation for clear input/output comparison  
  - Fine-grained validation for rows, columns, and boxes  
  - Detailed error handling for invalid or unsolvable boards

# 🗼 Tower of Hanoi Solver  
`fcc-reimagined-projects/TowerOfHanoi.py`

**Unique Approach**: Iterative disk movement with manual cycle tracking and dictionary-based towers  
- **Challenge**: Solve the Tower of Hanoi puzzle for any disk count using only lists and dictionaries  
- **Innovation**: Added a cycle-based smallest disk movement and custom legal move detection without recursion  
- **Key Features**:  
  - Iterative solution for both even and odd disk counts  
  - Manual tracking of disk locations for efficient moves  
  - Interactive CLI for user input and repeated runs  
  - Comprehensive input validation and error handling