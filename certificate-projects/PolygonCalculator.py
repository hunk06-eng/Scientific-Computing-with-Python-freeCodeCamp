class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2*(self.height+self.width)

    def get_diagonal(self):
        return (self.height**2+self.width**2)**0.5

    def get_picture(self, round_floats=False):
        if self.width > 50 or self.height > 50:
            return 'Too big for picture.'
        each_line = "*"*self.width if not round_floats else "*" * round(self.width)
        output_str = [each_line for _ in range(self.height if not round_floats else round(self.height))]

        return "\n".join(output_str) + "\n"

    def get_amount_inside(self, shape):
        return self.get_area() // shape.get_area()

class Square(Rectangle):
    def __init__(self, side_len):
        super().__init__(side_len, side_len)

    def __str__(self):
        return f"Square(side={self.width})"

    def set_side(self, new_side):
        self.width = new_side
        self.height = new_side

    def set_width(self, new_width):
        super().set_width(new_width)
        self.height = new_width

    def set_height(self, new_height):
        super().set_height(new_height)
        self.width = new_height

if __name__ == "__main__":
    print("This script performs various operations on two shapes: Squares and Rectangles.")
    print("It has less to do with logic, more to do with inheritance and OOP.")

    shapes = []
    def create_shape(shape, rectangle=False, square=False):
        print("Make sure to enter lengths without units such as cm or km, just pure digits.")
        if rectangle:
            width = input("Enter rectangle width: ").strip()
            height = input("Enter rectangle height: ").strip()
            try:
                shape.set_width(float(width))
                shape.set_height(float(height))
            except ValueError:
                return False
        if square:
            side_len = input("Enter square side length: ").strip()
            try:
                shape.set_side(float(side_len))
            except ValueError:
                return False

        return True

    def show_shapes(shapes_list):
        print("Choose a shape based on the number that represents it (not the name)")
        print("1 for the 1st shape, 2 for the 2nd shape, etc...")

        for idx, shape in enumerate(shapes_list):
            print(f"({idx+1}) {shape}")


    while True:
        print("(1) To create a rectangle.")
        print("(2) To create a square.")
        print("(3) To get area of a shape")
        print("(4) To get perimeter of a shape")
        print("(5) To get diagonal of a shape")
        print("(6) To get a picture of the shape (each * represents 1 digit)")
        print("(7) To see how many shapes fit in a shape (e.g. how many squares fit in a rectangle)")
        print("(8) To see shapes list")
        print("(9) To erase shapes list")
        print("(10) To exit script")

        usr_choice = input("Enter a choice from the menu (a digit only): ").strip()
        if usr_choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            print("Invalid choice, you can only enter a digit from 1 to 10, please try again.")
            continue

        if usr_choice == '1':
            rect = Rectangle(0, 0)
            if not create_shape(rect, True, False):
                print("Error! Probably because either the width or height is an invalid number that cannot be converted to a float")
                print("Try again, remember to not add units like 44m or 44.5cm")
                continue
            else:
                shapes.append(rect)
        elif usr_choice == '2':
            sqr = Square(0)
            if not create_shape(sqr, False, True):
                print("Error! Probably because either the side length is an invalid number that cannot be converted to a float")
                print("Try again, remember to not add units like 44m or 44.5cm")
                continue
            else:
                shapes.append(sqr)
        elif usr_choice == '3':
            show_shapes(shapes)
            req_shape = input("Enter a digit that represents the shape shown above to calculate its area: ")
            if not req_shape.isnumeric():
                print("Error. This is not a digit. If I want the first shape, I'll simply input 1\nTry again..")
                continue
            req_shape = shapes[int(req_shape)-1]
            print(f"The area for {req_shape} is {req_shape.get_area()}")
        elif usr_choice == '4':
            show_shapes(shapes)
            req_shape = input("Enter a digit that represents the shape shown above to calculate its perimeter: ")
            if not req_shape.isnumeric():
                print("Error. This is not a digit. If I want the first shape, I'll simply input 1\nTry again..")
                continue
            req_shape = shapes[int(req_shape)-1]
            print(f"The perimeter for {req_shape} is {req_shape.get_perimeter()}")
        elif usr_choice == '5':
            show_shapes(shapes)
            req_shape = input("Enter a digit that represents the shape shown above to calculate its diagonal: ")
            if not req_shape.isnumeric():
                print("Error. This is not a digit. If I want the first shape, I'll simply input 1\nTry again..")
                continue
            req_shape = shapes[int(req_shape)-1]
            print(f"The diagonal for {req_shape} is {req_shape.get_diagonal()}")
        elif usr_choice == '6':
            show_shapes(shapes)
            req_shape = input("Enter a digit that represents the shape shown above to output its picture: ")
            if not req_shape.isnumeric():
                print("Error. This is not a digit. If I want the first shape, I'll simply input 1\nTry again..")
                continue
            req_shape = shapes[int(req_shape)-1]
            print(f"The picture for {req_shape} is:\n{req_shape.get_picture(True)}")
        elif usr_choice == '7':
            show_shapes(shapes)
            parent_shape = input("Enter a digit that represents the parent shape (The one that will be filled): ")
            fill_in_parent = input("Enter a digit that represents the shape you want to place inside the parent shape, so we can calculate how many of them will fit: ")
            if not parent_shape.isnumeric() or not fill_in_parent.isnumeric():
                print("Error. This is not a digit. If I want the first shape, I'll simply input 1\nTry again..")
                continue
            parent_shape = shapes[int(parent_shape)-1]
            fill_in_parent = shapes[int(fill_in_parent)-1]
            print(f"Around {parent_shape.get_amount_inside(fill_in_parent)} shapes fit in the parent shape {parent_shape}")
        elif usr_choice == '8':
            print(f"Your shapes: {[str(shape) for shape in shapes]}")
        elif usr_choice == '9':
            shapes = []
            print("Shapes list erased successfully.")
        else:
            print("Exiting script...")
            break

        print("\n")