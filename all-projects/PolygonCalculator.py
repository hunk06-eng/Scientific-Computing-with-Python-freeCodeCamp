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
        return (self.height**2+self.width**2)**-2

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return 'Too big for picture.'
        each_line = "*"*self.width
        output_str = [each_line for _ in range(self.height)]

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

rect = Rectangle(10, 5)
print(rect.get_area())
rect.set_height(3)
print(rect.get_perimeter())
print(rect)
print(rect.get_picture())

sq = Square(9)
print(sq.get_area())
sq.set_side(4)
print(sq.get_diagonal())
print(sq)
print(sq.get_picture())

rect.set_height(8)
rect.set_width(16)
print(rect.get_amount_inside(sq))