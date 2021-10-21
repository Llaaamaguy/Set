class Card:
    SHAPES = ["diamond", "squiggle", "oval"]
    NUMS = [1, 2, 3]
    SHADE = ["solid", "striped", "open"]
    COLOR = ["green", "purple", "red"]

    def __init__(self, num, shade, color, shape):
        self.num = num
        self.shape = shape
        self.shade = shade
        self.color = color

    def __repr__(self):
        return f"{self.num} {self.shade} {self.color} {self.shape}"

    def __str__(self):
        return f"Card: {self.num} {self.shade} {self.color} {self.shape}"
