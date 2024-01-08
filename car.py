from math import sin, cos, pi

class Car:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    
    def go(self):
        self.x += cos(self.r)
        self.y += sin(self.r)

    def turn(self, r):
        self.r = ((self.r + r) + (2 * pi)) % (2*pi)

    def polygon_points(self):
        return (
            (self.x + (20*cos(self.r)), self.y + (20*sin(self.r))),
            (self.x, self.y)
        )