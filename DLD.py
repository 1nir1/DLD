import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from math import hypot
from Models.Point import Point
from Models.Line import Line
from Models.DataExtractor import ExtractPointsByArea
from Models.IO import GetCommandLineParams

def MovingWindow(n, iterable):
  start, stop = 0, n
  while stop <= len(iterable):
      yield iterable[start:stop]
      start += 1
      stop += 1

def CreateLinesFromPoints(points):
    lines = []

    for point in points:
        validLines = [line for line in lines if line.CanPointBeAdded(point)]
        lineProximities = {line.GetPointProximityValue(point): line for line in validLines}

        if len(lineProximities) > 0:
            firstKey = sorted(lineProximities.keys())[0]
            bestLine = lineProximities[firstKey]
            bestLine.AddPoint(point)
        else:   
            line = Line()
            line.AddPoint(point)
            lines.append(line)

    filteredLines = [line for line in lines if line.Size() > 1]
    return filteredLines

# get array of fileNames instead of fileName
(fileName, minArea, maxArea, deltaXFactor) = GetCommandLineParams()

# then run this code under: "for fileName in fileNames:"
points = ExtractPointsByArea(fileName, minArea, maxArea)
points.sort(key=lambda point: point._x)
deltaX = points[-1]._x - points[0]._x

lines = CreateLinesFromPoints(points)

wereLinesMerged = True
while wereLinesMerged:
    linesAfterMerge = []
    lines.sort(key=lambda line: line.GetAverageYPoint())
    wereLinesMerged = False
    for coupleOflines in MovingWindow(2, lines):
        if Line.CanLinesBeMerged(coupleOflines[0], coupleOflines[1]):
            linesAfterMerge.append(coupleOflines[0] + coupleOflines[1])
            lines.remove(coupleOflines[0])
            lines.remove(coupleOflines[1])
            wereLinesMerged = True
    lines = lines + linesAfterMerge

#mergedLines = [coupleOflines[0] + coupleOflines[1] if Line.CanLinesBeMerged(coupleOflines[0], coupleOflines[1]) else coupleOflines[0] for coupleOflines in MovingWindow(2, lines)]
#lines = mergedLines

with open('Dest/out1.txt', 'w') as f:
    for line in lines:
        (xCoordinates, yCoordinates) = line.GetCoordiantes()
        x = np.asarray(xCoordinates)
        y = np.asarray(yCoordinates)
        b, m = polyfit(x, y, 1)
        yValuesAfterPolyfit = b + m * x
        lineLength = hypot(x[-1] - x[0], yValuesAfterPolyfit[-1] - yValuesAfterPolyfit[0])
        if lineLength < deltaXFactor * deltaX:
            continue

        plt.plot(x, y)
        plt.plot(x, yValuesAfterPolyfit, '-')
        print("new line, average radius: {0}, biggestYPoint {1}, smallestYPoint {2}".format(line.GetAverageRadius(), line._biggestYPoint, line._smalletYPoint), file=f)
        print(line._points, file=f)
        
        linearReprLine = Line([Point(xVal,yVal,0) for xVal,yVal in zip(x, yValuesAfterPolyfit)])
        line.FilterOutFarPoints(linearReprLine)
        print("yabadaba")
        (xCoordinatesAfterLinear, yCoordinatesAfterLinear) = line.GetCoordiantes()
        xAfterLinear = np.asarray(xCoordinatesAfterLinear)
        yAfterLinear = np.asarray(yCoordinatesAfterLinear)
        plt.plot(xAfterLinear, yAfterLinear)

ax=plt.gca()
ax.xaxis.tick_top() 
ax.invert_yaxis()
plt.show() 
