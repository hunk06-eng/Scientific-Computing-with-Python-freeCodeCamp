This repository contains a collection of Python projects that I built to practice different programming concepts and algorithms while taking fCC (Python for Scientific Computing certificate). Each project tackles a real problem and includes plenty of comments to explain whats happening.

Luhn Algorithm (LuhnAlgorithm.py): An algorithm used to validate credit card numbers, SSN, and other ID numbers. The algorithm checks every second digit from right to left, doubles it, and if its bigger than 9, subtracts 9 from it. Then it sums everything. if the total is dividable by 10, the number is valid. I included multiple test cases to make sure it handles weird inputs like empty strings and random text.

Root Finding by Bisection Method (RootByBisectionMethod.py): This script finds square roots using a method that is basically like binary search. You start with an interval and keep cutting it in half until you get close enough to an answer. Added lots of comments explaining the math behind it. And created a nice UI if you don't want to specify tolerance or max_iterations.

Case Converter (CaseConverter.py): Used for converting between PascalCase, camelCase, and snake_case. The tricky part was handling edge cases like multiple underscores behind each other, or digits in the middle of an identifier. I used isalnum() to filter out weird characters and added a bunch of error checking for invalid inputs.

Vigenere Cipher (VigenereEncryption.py): Some classic cryptography cuz why not. It shifts letters based on a key word, while preserving spaces and punctuation. Used some basic ASCII math to handle both uppercase and lowercase letters properly. Added test cases with some sample text to make sure everything works. Read warnings please, don't use this for sensitive info!

Expense Tracker (ExpensesTracker.py): Unlike the freeCodeCamp version, I expanded this script with way more features. Now it can save data to local files, detects and removes duplicate categories, and has better error handling. I used dictionaries to organize everything by category and added both append and overwrite modes in the log file for saving data. Pretty useful for tracking personal expenses. But a notepad works great too.

Password Generator (PasswordGeneratorRegex.py): This is a customizable and simple password generator. It uses Python's secrets module for cryptographic randomness and regular expressions for validation. The script generates passwords with a mix of letters, digits, and symbols. Users can specify the desired length of the password and the proportions of each character type. It also shuflles characters in the generated password and breaks predictable patterns. User-friendly CLI.

Note: This script is for educational purposes and should not be used for critical security needs.

Arithmetic Formatter (ArithmeticFormatter.py): it formats basic arithmetic problems such as addition and subtraction for display. This script adheres to the requirements specified by the freeCodeCamp certification project: supports up to 5 arithmetic problems, optionally shows answer, operands cannot exceed four digits, only operators allowed are ( + or -).

I'll add more projects soon.

What I'm Proud Of
1) Good error handling
2) Good algorithms
3) Clean code structure
4) User friendly design
5) Built-in testing
6) Detailed comments for fellow learners

Thank you for reading! Hope you like my work.
