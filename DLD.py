import os
import matplotlib.pyplot as plt

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

def MergeCloseLines(lines):
    wereLinesMerged = True
    while wereLinesMerged:
        linesAfterMerge = []
        # we sort by the average y point, becuase it is a "blocking-factor" if line1 and line3 have line2 btw them, they cannot be merged!
        lines.sort(key=lambda line: line.GetAverageYPoint())
        wereLinesMerged = False
        for coupleOflines in MovingWindow(2, lines):
            if Line.CanLinesBeMerged(coupleOflines[0], coupleOflines[1]):
                linesAfterMerge.append(coupleOflines[0] + coupleOflines[1])
                lines.remove(coupleOflines[0])
                lines.remove(coupleOflines[1])
                wereLinesMerged = True
        lines = lines + linesAfterMerge
    
    return lines

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

(fileNames, minArea, maxArea, deltaXFactor) = GetCommandLineParams()
for fileName in fileNames:
    baseFileName = os.path.splitext(fileName)[0]

    points = ExtractPointsByArea("Source/{0}".format(fileName), minArea, maxArea)
    points.sort(key=lambda point: point._x)
    deltaX = points[-1]._x - points[0]._x

    lines = CreateLinesFromPoints(points)
    lines = MergeCloseLines(lines)

    with open('Dest/{0}.txt'.format(baseFileName), 'w') as f:
        for line in lines:
            linearReprLine = line.GetLinearReprLine()
            lineLength = linearReprLine.GetLineLength()
            
            if lineLength < deltaXFactor * deltaX:
                continue
            
            (x, y) = line.GetCoordiantes()
            plt.plot(x,y)
            (linearX, linearY) = linearReprLine.GetCoordiantes()
            plt.plot(linearX, linearY, '-')
            
            print("new line, averageYPoint: {0}, average radius: {1}, biggestYPoint {2}, smallestYPoint {3}".format(line.GetAverageYPoint(), line.GetAverageRadius(), line._biggestYPoint, line._smallestYPoint), file=f)
            print(line._points, file=f)
            
            line.FilterOutFarPoints(linearReprLine)

            (xAfterFilteringFarPoints, yAfterFilteringFarPoints) = line.GetCoordiantes()
            plt.plot(xAfterFilteringFarPoints, yAfterFilteringFarPoints)

    ax=plt.gca()
    ax.xaxis.tick_top() 
    ax.invert_yaxis()
    plt.savefig('Dest/{0}.png'.format(baseFileName))
    plt.clf()
    plt.cla()
    plt.close()
    #plt.show()
