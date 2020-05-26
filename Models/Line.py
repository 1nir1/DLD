import statistics
import numpy as np
import Models.Consts

from Models.Point import Point
from math import sqrt
from numpy.polynomial.polynomial import polyfit
from math import hypot

def _getDistanceBetweenTwoPoints(point1, point2, xFactor = 1):
    # sqrt((x2 − x1)^2 + (y2 − y1)^2) − (r2 + r1)
    distanceBetweenTwoPoints = sqrt(xFactor * pow((point1.x - point2.x), 2) + pow((point1.y - point2.y), 2)) - (point1.radius + point2.radius)
    return distanceBetweenTwoPoints

def _getAverage(values):
        averageValues = statistics.median(values)
        roundedAverageValues = round(averageValues, Models.Consts.ROUNDED_DIGITS_NUMBER)
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

    def __str__(self):
        return "averageYPoint: {0}, average radius: {1}, biggestYPoint {2}, smallestYPoint {3}".format(self.GetAverageYPoint(), self.GetAverageRadius(), self._biggestYPoint, self._smallestYPoint)

    def __repr__(self):
        return str(self)

    @property
    def points(self):
        return self._points

    @property    
    def smallestYPoint(self):
        return self._smallestYPoint

    @property
    def biggestYPoint(self):
        return self._biggestYPoint

    @property
    def smallestXPoint(self):
        return self._smallestXPoint

    @property
    def biggestXPoint(self):
        return self._biggestXPoint        

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

    def CanPointBeAdded(self, point, radiusFactor = 1):
        if len(self._points) == 0:
            return True
        
        if point.y - point.radius * radiusFactor <= self._biggestYPoint.y + self._biggestYPoint.radius * radiusFactor and \
             point.y + point.radius * radiusFactor >= self._smallestYPoint.y - self._smallestYPoint.radius * radiusFactor:
            return True
        
        return False

    def GetPointProximityValue(self, point):
        proximityValues = map(lambda x: _getDistanceBetweenTwoPoints(x, point, Models.Consts.POINT_DISTANCE_X_FACTOR), self._points)
        proximityValue = min(proximityValues)
        roundedProximityValue = round(proximityValue, Models.Consts.ROUNDED_DIGITS_NUMBER)
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
                if firstLineAverageY - firstLineAverageRadius * Models.Consts.MERGE_RADIUS_FACTOR < secondLineAverageY + secondLineAverageRadius * Models.Consts.MERGE_RADIUS_FACTOR:
                    return True
            else:
                if firstLineAverageY + firstLineAverageRadius * Models.Consts.MERGE_RADIUS_FACTOR > secondLineAverageY - secondLineAverageRadius * Models.Consts.MERGE_RADIUS_FACTOR:
                    return True

        return False
