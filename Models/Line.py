import statistics
from math import sqrt

def _getDistanceBetweenTwoPoints(point1, point2):
    # TODO - check algo
    # sqrt((x2 − x1)^2 + (y2 − y1)^2) − (r2 + r1)
    distanceBetweenTwoPoints = sqrt(pow((point1._x - point2._x), 2)+ pow((point1._y - point2._y ), 2)) - (point1._radius + point2._radius)
    return distanceBetweenTwoPoints

def _getAverage(values):
        averageValues = statistics.median(values)
        roundedAverageValues = round(averageValues, 4)
        return roundedAverageValues


class Line:
    def __init__(self, points = None):
        if points is None:
            self._points = []
            self._smallestYPoint = None
            self._biggestYPoint = None
            self._smallestXPoint = None
            self._biggestXPoint = None
        else:
            self._points = points
            self._smallestYPoint = min(points, key=lambda point: point._y)
            self._biggestYPoint = max(points, key=lambda point: point._y)
            self._smallestXPoint = min(points, key=lambda point: point._x)
            self._biggestXPoint = max(points, key=lambda point: point._x)

    def __add__(self, otherLine):
        allPoints = self._points + otherLine._points
        allPoints.sort(key=lambda point: point._x)
        return Line(allPoints)

    def AddPoint(self, point):
        self._points.append(point)
        self._biggestXPoint = point

        if len(self._points) == 1:
            self._smallestYPoint = point
            self._biggestYPoint = point
            self._smallestXPoint = point
            
        if point._y + point._radius > self._biggestYPoint._y + self._biggestYPoint._radius:
            self._biggestYPoint = point
            
        if point._y - point._radius < self._smallestYPoint._y - self._smallestYPoint._radius:
            self._smallestYPoint = point

    def RemovePoint(self, point):
        self._points.remove(point)

        if len(self._points) == 0:
            self._smallestYPoint = None
            self._biggestYPoint = None
            self._smallestXPoint = None
            self._biggestXPoint = None
        else:
            if self._smallestYPoint == point:
                self._smallestYPoint = min(self._points, key=lambda point: point._y)

            if self._biggestYPoint == point:
                self._biggestYPoint = max(self._points, key=lambda point: point._y)

            if self._smallestXPoint == point:
                self._smallestXPoint = min(self._points, key=lambda point: point._x)

            if self._biggestXPoint == point:
                self._biggestXPoint = max(self._points, key=lambda point: point._x)

    def CanPointBeAdded(self, point):
        if len(self._points) == 0:
            return True
        
        if point._y - point._radius <= self._biggestYPoint._y + self._biggestYPoint._radius and point._y + point._radius >= self._smallestYPoint._y - self._smallestYPoint._radius:
            return True
        
        return False

    def GetPointProximityValue(self, point):
        #distanceFromBiggestYPoint = GetDistanceBetweenTwoPoints(point, self._biggestYPoint)
        #distanceFromSmallestYPoint = GetDistanceBetweenTwoPoints(point, self._smallestYPoint)
        proximityValue = _getDistanceBetweenTwoPoints(point, self._biggestXPoint) #min(distanceFromBiggestYPoint, distanceFromSmallestYPoint)
        roundedProximityValue = round(proximityValue, 4)
        return roundedProximityValue
    
    def GetCoordiantes(self):
        outputX = [point._x for point in self._points]
        outputY = [point._y for point in self._points]

        return (outputX, outputY)

    def GetAverageRadius(self):
        radiusValues = [point._radius for point in self._points]
        return _getAverage(radiusValues)

    def GetAverageYPoint(self):
        yValues = [point._y for point in self._points]
        return _getAverage(yValues)

    def Size(self):
        return len(self._points)
    
    def FilterOutFarPoints(self, comparedLine):
        averageRadius = self.GetAverageRadius()
        for myPoint, comparedLinePoint in zip(self._points, comparedLine._points):
            if _getDistanceBetweenTwoPoints(myPoint, comparedLinePoint) > averageRadius:
                self.RemovePoint(myPoint)
    
    @staticmethod
    def CanLinesBeMerged(line1, line2):
        #return False
        if line1._smallestXPoint._x > line2._biggestXPoint._x or line2._smallestXPoint._x > line1._biggestXPoint._x:
            
            firstLineAverageRadius = line1.GetAverageRadius()
            firstLineAverageY = line1.GetAverageYPoint()

            secondLineAverageRadius = line2.GetAverageRadius()
            secondLineAverageY = line2.GetAverageYPoint()

            if firstLineAverageY > secondLineAverageY:
                if firstLineAverageY - firstLineAverageRadius*10 < secondLineAverageY + secondLineAverageRadius*10:
                    print("merged1")
                    return True
            else:
                if firstLineAverageY + firstLineAverageRadius*10 > secondLineAverageY - secondLineAverageRadius*10:
                    print("merged2")
                    return True

        return False
