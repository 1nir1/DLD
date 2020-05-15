import statistics
from math import sqrt

def GetDistanceBetweenTwoPoints(point1, point2):
    # TODO - check algo
    # sqrt((x2 − x1)^2 + (y2 − y1)^2) − (r2 + r1)
    distanceBetweenTwoPoints = sqrt(pow((point1._x - point2._x), 2)+ pow((point1._y - point2._y ), 2)) - (point1._radius + point2._radius)
    return distanceBetweenTwoPoints

class Line:
    def __init__(self, points = None):
        if points is None:
            self._points = []
            self._smalletYPoint = None
            self._biggestYPoint = None
            self._lastPointAdded = None
        else:
            self._points = points
            self._smallestYPoint = min(points, key=lambda point: point._y)
            self._biggestYPoint = max(points, key=lambda point: point._y)
            self._lastPointAdded = max(points, key=lambda point: point._x)

    def AddPoint(self, point):
        self._points.append(point)
        self._lastPointAdded = point

        if len(self._points) == 1:
            self._biggestYPoint = point
            self._smalletYPoint = point
            
        if point._y + point._radius > self._biggestYPoint._y + self._biggestYPoint._radius:
            self._biggestYPoint = point
            
        if point._y - point._radius < self._smalletYPoint._y - self._smalletYPoint._radius:
            self._smalletYPoint = point

    def RemovePoint(self, point):
        self._points.remove(point)

        if len(self._points) == 0:
            self._smalletYPoint = None
            self._biggestYPoint = None
            self._lastPointAdded = None
        else:
            if self._biggestYPoint == point:
                self._biggestYPoint = max(self._points, key=lambda point: point._y)

            if self._smalletYPoint == point:
                self._smallestYPoint = min(self._points, key=lambda point: point._y)

            if self._lastPointAdded == point:
                self._lastPointAdded = max(self._points, key=lambda point: point._x)

    def CanPointBeAdded(self, point):
        if len(self._points) == 0:
            return True
        
        if point._y - point._radius <= self._biggestYPoint._y + self._biggestYPoint._radius and point._y + point._radius >= self._smalletYPoint._y - self._smalletYPoint._radius:
            return True
        
        return False

    def GetPointProximityValue(self, point):
        #distanceFromBiggestYPoint = GetDistanceBetweenTwoPoints(point, self._biggestYPoint)
        #distanceFromSmallestYPoint = GetDistanceBetweenTwoPoints(point, self._smalletYPoint)
        proximityValue = GetDistanceBetweenTwoPoints(point, self._lastPointAdded) #min(distanceFromBiggestYPoint, distanceFromSmallestYPoint)
        roundedProximityValue = round(proximityValue, 4)
        return roundedProximityValue
    
    def GetCoordiantes(self):
        outputX = [point._x for point in self._points]
        outputY = [point._y for point in self._points]

        return (outputX, outputY)

    def GetAverageRadius(self):
        radiusValues = [point._radius for point in self._points]
        averageRadius = statistics.median(radiusValues)
        roundedAverageRadius = round(averageRadius, 4)
        return roundedAverageRadius

    def Size(self):
        return len(self._points)
    
    def FilterOutFarPoints(self, comparedLine):
        averageRadius = self.GetAverageRadius()
        for myPoint, comparedLinePoint in zip(self._points, comparedLine._points):
            if GetDistanceBetweenTwoPoints(myPoint, comparedLinePoint) > averageRadius:
                self.RemovePoint(myPoint)