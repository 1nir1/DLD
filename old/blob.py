import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np
from numpy.polynomial.polynomial import polyfit
from math import hypot

class Point: 
    def __init__(self, x, y, feret):
        self._x = float(x)
        self._y = float(y)
        self._radius = float(feret) / 2

    def __str__(self):
        return "({0},{1}), {2}".format(self._x, self._y, self._radius)

    def __repr__(self):
        return str(self)

class Line:
    def __init__(self):
        self._points = []
        self._smallestYPoint = None
        self._biggestYPoint = None

    def TryToAddPoint(self, point):
        if len(self._points) == 0:
            self._points.append(point)
            self._biggestYPoint = point
            self._smallestYPoint = point
            return True
        
        if point._y - point._radius <= self._biggestYPoint._y + self._biggestYPoint._radius and point._y + point._radius >= self._smallestYPoint._y - self._smallestYPoint._radius:
            self._points.append(point)
            
            if point._y + point._radius > self._biggestYPoint._y + self._biggestYPoint._radius:
                self._biggestYPoint = point
            
            if point._y - point._radius < self._smallestYPoint._y - self._smallestYPoint._radius:
                self._smallestYPoint = point
            
            return True
        
        return False
    
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

# TODO CONFIGURABLE BY USER #
minArea = 1
maxArea = 15
#############################

points = []
with open('Results-filter_new.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        area = row['Area']
        xMid = row['XM']
        yMid = row['YM']
        feret = row['Feret']
        if  xMid != '' and  yMid != '' and feret != '' and area != '':
            floatArea = float(area)
            if floatArea > minArea and floatArea < maxArea:
                point = Point(xMid, yMid, feret)
                points.append(point)

points.sort(key=lambda point: point._x)
deltaX = points[-1]._x - points[0]._x

lines = []
i = 0
for point in points:
    foundLine = False
    for line in lines:
        if(line.TryToAddPoint(point)):
            # INSTEAD - get result from line - is the point ok to be added?
            # if so, add line to array of candidates, don't break the check - continue adding lines to that array

            foundLine = True
            break
    
    if foundLine is False:
        # change check to - "is array of fit lines empty"
        line = Line()
        line.TryToAddPoint(point)
        lines.append(line)
        #if added here - break
    
    # add test here - which line from the array is the fittest - add the point to it

filteredLines = [line for line in lines if line.Size() > 1]
with open('out.txt', 'w') as f:
    for line in filteredLines:
        (xCoordinates, yCoordinates) = line.GetCoordiantes()
        x = np.asarray(xCoordinates) 
        y = np.asarray(yCoordinates)
        b, m = polyfit(x, y, 1)
        yValuesAfterPolyfit = b + m * x
        lineLength = hypot(x[-1] - x[0], yValuesAfterPolyfit[-1] - yValuesAfterPolyfit[0])
        if lineLength < 0.7 * deltaX:
            continue
        plt.plot(x, y)
        plt.plot(x, yValuesAfterPolyfit, '-')
        print("new line, average radius: {0}".format(line.GetAverageRadius()), file=f)
        print(line._points, file=f)
        # linearLine = Line(x, yValuesAfterPolyfit)
        dictionary = dict(zip(x, yValuesAfterPolyfit))
        #print(dictionary)
        #dic = { x : yValuesAfterPolyfit}
        # TODO line.FilterPointsAccordingToyValuesAfterPolyfit(new Dic {x : yValuesAfterPolyfit})

ax=plt.gca()
ax.xaxis.tick_top() 
ax.invert_yaxis()
plt.show() 
