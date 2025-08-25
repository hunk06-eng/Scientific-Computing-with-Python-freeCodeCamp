# certification project
import random

class Hat:
    def __init__(self, **kwargs):
        self.colors = [color for color in kwargs.keys()]
        self.contents = [color for color in kwargs for _ in range(kwargs[color])]

    def draw(self, num_of_balls_to_draw):
        if num_of_balls_to_draw > len(self.contents):
            balls_drawn = self.contents
            self.contents = []
            return balls_drawn

        balls_drawn = []
        for _ in range(num_of_balls_to_draw):
            to_remove = random.choice(self.contents)
            self.contents.remove(to_remove)
            balls_drawn.append(to_remove)

        return balls_drawn


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    number_of_passes = 0
    contents_original = hat.contents[:]

    for _ in range(num_experiments):
        flag_for_pass = True
        draw_result = hat.draw(num_balls_drawn)
        draw_results_count = {color: 0 for color in hat.colors}

        for color in draw_result:
            draw_results_count[color] += 1

        for color, result in draw_results_count.items():
            if color in expected_balls.keys():
                if result < expected_balls[color]:
                    flag_for_pass = False

        hat.contents = contents_original[:]
        if flag_for_pass:
            number_of_passes += 1

    return number_of_passes / num_experiments

if __name__ == "__main__":
    print("This script calculates probability by performing random draws multiple times, then seeing how many times we get the desired output compared to the total amount of draws.")
    print("The more random experiments we perform, the more accurate the result is.\n")

    while True:
        box = {}
        expected_box = {}

        contents = input("Enter each content name in the object we are drawing from.\nName them using distinctive feature e.g. ( red,yellow,green ) for balls or ( queen,king,joker ) for cards.\nMake sure to separate content names by a single comma (no whitespaces in between): ").strip().title().split(",")
        try:
            for content in contents:
                number_of = input(f"Enter the total number of {content}s that exist in the object we're drawing from: ").strip()
                if not number_of.isnumeric():
                    print("Invalid number. Must be an integer only. No characters or symbols")
                    raise ValueError
                number_of = int(number_of)
                if number_of <= 0:
                    print("Error! Invalid number. Can only be positive.")
                    raise ValueError
                box[content] = number_of
        except ValueError:
            print("Retrying...")
            continue

        print(f"These are your box contents: {box.keys()}")
        expected_by_name = input("Enter the contents you are expecting after draw, by their name e.g. ( red,yellow ) balls\nRemember to separate names by a single comma, no whitespaces: ").strip().title().split(",")
        try:
            for content in expected_by_name:
                number_of = input(f"Enter the number of {content}s that you are expecting per draw (at least): ").strip()
                if not number_of.isnumeric():
                    print("Invalid number. Must be an integer only. No characters or symbols")
                    raise ValueError
                number_of = int(number_of)
                if number_of <= 0:
                    print("Error! Invalid number. Can only be positive")
                    raise ValueError
                if number_of > box[content]:
                    print(f"Error! You can't expect {number_of} {content}s when you only have {box[content]} {content}s.")
                    raise ValueError
                expected_box[content] = number_of
        except ValueError:
            print("Retrying...")
            continue

        contents_to_draw = input("Enter the number of contents you'd like to draw per a single experiment\n(Must be not less than total expected contents amount): ")
        if not contents_to_draw.isnumeric():
            print("Invalid number. Must be an integer only. No characters or symbols")
            print("Retrying...")
            continue
        contents_to_draw = int(contents_to_draw)
        expected_total = sum(expected_box.values())
        if contents_to_draw < expected_total:
            print(f"Error! The number of contents drawn each time must not be less than the total expected contents.\nHow can you expect to draw {expected_total} contents when you only draw {contents_to_draw} contents each experiment...")
            print("Retrying...")
            continue
        number_of_experiments = input("Enter the number of experiments you'd like to run (recommended 3000<n<20000): ")
        if not number_of_experiments.isnumeric():
            print("Invalid number. Must be an integer only. No characters or symbols")
            print("Retrying...")
            continue
        number_of_experiments = int(number_of_experiments)
        while True:
            probability = experiment(Hat(**box), expected_box, contents_to_draw, number_of_experiments)
            print(f"Your calculated probability after {number_of_experiments} runs is: {probability} or {probability*100}%")
            usr_choice = input("Choose an option.\n( C ) to rerun experiment with same inputs/parameters.\n( R ) to start a new experiment with different inputs/parameters\n( Q ) to quit script completely\nYour choice: ").strip().upper()
            if usr_choice == 'C':
                continue
            elif usr_choice == 'R':
                break
            elif usr_choice == 'Q':
                exit()
            else:
                print("Invalid choice! Restarting script...")
                break

        print("\n")