import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from math import hypot
from Models.Point import Point
from Models.Line import Line
from Models.DataExtractor import ExtractPointsByArea
from Models.IO import GetCommandLineParams

(fileName, minArea, maxArea, deltaXFactor) = GetCommandLineParams()

points = ExtractPointsByArea(fileName, minArea, maxArea)
points.sort(key=lambda point: point._x)
deltaX = points[-1]._x - points[0]._x

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
with open('Dest/out1.txt', 'w') as f:
    for line in filteredLines:
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
        # linearLine = Line(x, yValuesAfterPolyfit)
        dictionary = dict(zip(x, yValuesAfterPolyfit))
        #print(dictionary)
        #dic = { x : yValuesAfterPolyfit}
        # TODO line.FilterPointsAccordingToyValuesAfterPolyfit(new Dic {x : yValuesAfterPolyfit})

ax=plt.gca()
ax.xaxis.tick_top() 
ax.invert_yaxis()
plt.show() 
