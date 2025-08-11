# certificate project
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

    return number_of_passes/num_experiments

hat = Hat(black=6, red=4, green=3)
probability = experiment(hat=hat,
                  expected_balls={'red':2,'green':1},
                  num_balls_drawn=5,
                  num_experiments=2000)
print(probability)