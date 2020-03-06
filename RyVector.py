import math

class RyVector:
    """ 2D homogenous vector. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 1

    def __add__(self, other):
        return RyVector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return RyVector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        t = type(other)
        if t == int or t == float:
            # multiplication
            return RyVector(self.x*other,self.y*other)
        elif t == RyVector:
            # dot product
            return (self.x * other.x) + (self.y * other.y)
        else:
            raise TypeError('Expected int/float/RyVector')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(%s, %s)' % (self.x,self.y)

    def point(self):
        return (self.x, self.y)

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def angle(self,other):
        dot = self*other
        mag = self.mag()*other.mag()
        return math.acos(dot/mag)

    # rotate RyVector theta degrees anti clockwise
    def rotate(self, theta):
        x_r = self.x * math.cos(theta) - self.y * math.sin(theta)
        y_r = self.x * math.sin(theta) + self.y * math.cos(theta)
        return RyVector(x_r, y_r)

    def normalize(self):
        mag = self.mag()
        if mag > 0:
            return RyVector(self.x/mag, self.y/mag)
        return RyVector(0, 0)

    def distance_to(self, other):
        return (other - self).mag()