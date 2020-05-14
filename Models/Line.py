import statistics

def GetDistanceBetweenTwoPoints(point1, point2):
    # TODO - check algo
    # sqrt((x2 − x1)^2 + (y2 − y1)^2) − (r2 + r1)
    distanceBetweenTwoPoints = abs(point1._y - point2._y ) - (point1._radius + point2._radius)
    return distanceBetweenTwoPoints

class Line:
    def __init__(self):
        self._points = []
        self._smalletYPoint = None
        self._biggestYPoint = None

    def TryToAddPoint(self, point):
        if len(self._points) == 0:
            self._points.append(point)
            self._biggestYPoint = point
            self._smalletYPoint = point
            return True
        
        if point._y - point._radius <= self._biggestYPoint._y + self._biggestYPoint._radius and point._y + point._radius >= self._smalletYPoint._y - self._smalletYPoint._radius:
            self._points.append(point)
            
            if point._y + point._radius > self._biggestYPoint._y + self._biggestYPoint._radius:
                self._biggestYPoint = point
            
            if point._y - point._radius < self._smalletYPoint._y - self._smalletYPoint._radius:
                self._smalletYPoint = point
            
            return True
        
        return False

    def GetPointProximityValue(self, point):
        distanceFromBiggestYPoint = GetDistanceBetweenTwoPoints(point, self._biggestYPoint)
        distanceFromSmallestYPoint = GetDistanceBetweenTwoPoints(point, self._smalletYPoint)
        proximityValue = min(distanceFromBiggestYPoint, distanceFromSmallestYPoint)
        roundedProximityValue = round(proximityValue, 4)
        return roundedProximityValue
    
    def GetCoordiantes(self):
        outputX = [point._x for point in self._points]
        outputY = [point._y for point in self._points]

        return (outputX, outputY)

    def GetAverageRadius(self):
        radiusValues = (point._radius for point in self._points)
        return statistics.median(radiusValues)

    def Size(self):
        return len(self._points)
    # def FilterPointsAccordingToyValuesAfterPolyfit(self, yValuesAfterPolyfit):
    #     averageRadius = self.GetAverageRadius()
    #     for point in self._points:
    #         if point._y < 