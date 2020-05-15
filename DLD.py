import matplotlib.pyplot as plt
import numpy as np
import argparse

from numpy.polynomial.polynomial import polyfit
from math import hypot
from Models.Point import Point
from Models.Line import Line
from Models.DataExtractor import ExtractPointsByArea

def GetCommandLineParams():
    parser=argparse.ArgumentParser(description='DewettingLineDetector')
    parser.add_argument('--fileName', nargs=1, type=str, default=None, help='The path for the csv source file')
    parser.add_argument('--minArea', type=float, default=0, help='Minimum area for circles - smaller circles will be filtered out. Default value is 0')
    parser.add_argument('--maxArea', type=float, default=float("inf"), help='Maximum area for circles - bigger circles will be filtered out. Default value is infinity')
    args=parser.parse_args()

    minArea = args.minArea
    maxArea = args.maxArea
    fileName = args.fileName
    fileName = fileName[0].replace("'","")
    return (fileName, minArea, maxArea)

(fileName, minArea, maxArea) = GetCommandLineParams()

points = ExtractPointsByArea(fileName, minArea, maxArea)
points.sort(key=lambda point: point._x)
deltaX = points[-1]._x - points[0]._x

lines = []

for point in points:
    validLines = [line for line in lines if line.CanPointBeAdded(point)]

    lineProximities = {line.GetPointProximityValue(point): line for line in validLines}
    print("lineProximities {0}".format(lineProximities))
        
    if len(lineProximities) > 0:
        firstKey = sorted(lineProximities.keys())[0]
        bestLine = lineProximities[firstKey]
        bestLine.AddPoint(point)
        # INSTEAD - get result from line - is the point ok to be added?
        # if so, add line to array of candidates, don't break the check - continue adding lines to that array
    else:   
        # change check to - "is array of fit lines empty"
        line = Line()
        line.AddPoint(point)
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
