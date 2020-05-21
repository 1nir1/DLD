import statistics
import numpy as np

from Models.Point import Point
from math import sqrt
from numpy.polynomial.polynomial import polyfit
from math import hypot

def _getDistanceBetweenTwoPoints(point1, point2):
    # TODO - check algo
    # sqrt((x2 − x1)^2 + (y2 − y1)^2) − (r2 + r1)
    distanceBetweenTwoPoints = sqrt(pow((point1.x - point2.x), 2)+ pow((point1.y - point2.y ), 2)) - (point1.radius + point2.radius)
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
            self._smallestYPoint = min(points, key=lambda point: point.y)
            self._biggestYPoint = max(points, key=lambda point: point.y)
            self._smallestXPoint = min(points, key=lambda point: point.x)
            self._biggestXPoint = max(points, key=lambda point: point.x)

    def __add__(self, otherLine):
        allPoints = self._points + otherLine._points
        allPoints.sort(key=lambda point: point.x)
        return Line(allPoints)

    def AddPoint(self, point):
        self._points.append(point)
        self._biggestXPoint = point

        if len(self._points) == 1:
            self._smallestYPoint = point
            self._biggestYPoint = point
            self._smallestXPoint = point
            
        if point.y + point.radius > self._biggestYPoint.y + self._biggestYPoint.radius:
            self._biggestYPoint = point
            
        if point.y - point.radius < self._smallestYPoint.y - self._smallestYPoint.radius:
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
                self._smallestYPoint = min(self._points, key=lambda point: point.y)

            if self._biggestYPoint == point:
                self._biggestYPoint = max(self._points, key=lambda point: point.y)

            if self._smallestXPoint == point:
                self._smallestXPoint = min(self._points, key=lambda point: point.x)

            if self._biggestXPoint == point:
                self._biggestXPoint = max(self._points, key=lambda point: point.x)

    def CanPointBeAdded(self, point):
        if len(self._points) == 0:
            return True
        
        if point.y - point.radius <= self._biggestYPoint.y + self._biggestYPoint.radius and point.y + point.radius >= self._smallestYPoint.y - self._smallestYPoint.radius:
            return True
        
        return False

    def GetPointProximityValue(self, point):
        proximityValue = _getDistanceBetweenTwoPoints(point, self._biggestXPoint)
        roundedProximityValue = round(proximityValue, 4)
        return roundedProximityValue
    
    def GetCoordiantes(self):
        xCoordinates = [point.x for point in self._points]
        yCoordinates = [point.y for point in self._points]
        
        x = np.asarray(xCoordinates)
        y = np.asarray(yCoordinates)

        return x, y

    def GetAverageRadius(self):
        radiusValues = [point.radius for point in self._points]
        return _getAverage(radiusValues)

    def GetAverageYPoint(self):
        yValues = [point.y for point in self._points]
        return _getAverage(yValues)

    def Size(self):
        return len(self._points)
    
    def FilterOutFarPoints(self, comparedLine):
        averageRadius = self.GetAverageRadius()
        myPoints = self._points.copy()
        for myPoint, comparedLinePoint in zip(myPoints, comparedLine._points):
            distance = _getDistanceBetweenTwoPoints(myPoint, comparedLinePoint)
            if  distance > averageRadius:
                #print("removed {0} because distance was {1} and averageRadius is {2} myPoint {3} otherPoint {4}".format(myPoint, distance, averageRadius, myPoint, comparedLinePoint))
                self.RemovePoint(myPoint)
    
    def GetLinearReprLine(self):
        (x, y) = self.GetCoordiantes()
        b, m = polyfit(x, y, 1)
        yValuesAfterPolyfit = b + m * x

        linearReprLine = Line([Point(xVal,yVal,0) for xVal,yVal in zip(x, yValuesAfterPolyfit)])
        return linearReprLine

    def GetLineLength(self):
        lineLength = hypot(self._biggestXPoint.x - self._smallestXPoint.x, self._biggestYPoint.y - self._smallestYPoint.y)
        return lineLength

    @staticmethod
    def CanLinesBeMerged(line1, line2):
        if line1._smallestXPoint.x > line2._biggestXPoint.x or line2._smallestXPoint.x > line1._biggestXPoint.x:
            
            firstLineAverageRadius = line1.GetAverageRadius()
            firstLineAverageY = line1.GetAverageYPoint()

            secondLineAverageRadius = line2.GetAverageRadius()
            secondLineAverageY = line2.GetAverageYPoint()

            if firstLineAverageY > secondLineAverageY:
                if firstLineAverageY - firstLineAverageRadius*10 < secondLineAverageY + secondLineAverageRadius*10:
                    return True
            else:
                if firstLineAverageY + firstLineAverageRadius*10 > secondLineAverageY - secondLineAverageRadius*10:
                    return True

        return False
