from math import sqrt

class Point: 
    def __init__(self, x, y, feret):
        self._x = float(x)
        self._y = float(y)
        self._radius = float(feret) / 2

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def radius(self):
        return self._radius
        
    def __eq__(self, other): 
        if not isinstance(other, Point):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self._x == other._x and self._y == other._y and self._radius == other._radius

    def __str__(self):
        return "({0},{1}), {2}".format(self._x, self._y, self._radius)

    def __repr__(self):
        return str(self)

    @staticmethod
    def GetDistanceBetweenTwoPoints(point1, point2, xFactor = 1):
        # sqrt((x2 − x1)^2 + (y2 − y1)^2) − (r2 + r1)
        distanceBetweenTwoPoints = sqrt(xFactor * pow((point1.x - point2.x), 2) + pow((point1.y - point2.y), 2)) - (point1.radius + point2.radius)
        return distanceBetweenTwoPoints
    