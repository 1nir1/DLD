import os
import matplotlib.pyplot as plt
import itertools

from Models.Point import Point
from Models.Line import Line
from Models.DataExtractor import ExtractPointsByArea
from Models.IO import GetCommandLineParams
from pathlib import Path

def UniqueFile(basename, ext):
    actualname = "%s.%s" % (basename, ext)
    c = itertools.count()
    while os.path.exists(actualname):
        actualname = "%s (%d).%s" % (basename, next(c), ext)
    return actualname

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
    points.sort(key=lambda point: point.x)
    deltaX = points[-1].x - points[0].x

    lines = CreateLinesFromPoints(points)
    lines = MergeCloseLines(lines)

    destPath = "Dest/{0}".format(baseFileName)
    Path(destPath).mkdir(parents=True, exist_ok=True)
    baseName = "{0}/{1}".format(destPath, baseFileName)

    with open(UniqueFile(baseName,"txt"), 'w') as f:
        for index,line in enumerate(lines):
            linearReprLine = line.GetLinearReprLine()
            lineLength = linearReprLine.GetLineLength()
            
            if lineLength < deltaXFactor * deltaX:
                continue
            
            (x, y) = line.GetCoordiantes()
            plt.plot(x,y, label="{0} raw".format(index))
            (linearX, linearY) = linearReprLine.GetCoordiantes()
            plt.plot(linearX, linearY, '-', label="{0} linear".format(index))
            
            print("raw line index:{0}, averageYPoint: {1}, average radius: {2}, biggestYPoint {3}, smallestYPoint {4}".format(index, line.GetAverageYPoint(), line.GetAverageRadius(), line.biggestYPoint, line.smallestYPoint), file=f)
            print(line.points, file=f)
            print("linear line index:{0}, averageYPoint: {1}, average radius: {2}, biggestYPoint {3}, smallestYPoint {4}".format(index, linearReprLine.GetAverageYPoint(), linearReprLine.GetAverageRadius(), linearReprLine.biggestYPoint, linearReprLine.smallestYPoint), file=f)
            print(linearReprLine.points, file=f)
            
            line.FilterOutFarPoints(linearReprLine)
            print("afterFilteartion line index:{0}, averageYPoint: {1}, average radius: {2}, biggestYPoint {3}, smallestYPoint {4}".format(index, line.GetAverageYPoint(), line.GetAverageRadius(), line.biggestYPoint, line.smallestYPoint), file=f)
            print(line.points, file=f)
            
            (xAfterFilteringFarPoints, yAfterFilteringFarPoints) = line.GetCoordiantes()
            plt.plot(xAfterFilteringFarPoints, yAfterFilteringFarPoints, label="{0} after filteration".format(index))

    ax=plt.gca()
    ax.xaxis.tick_top() 
    ax.invert_yaxis()
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 6})

    plt.savefig(UniqueFile(baseName, "pdf"))
    plt.clf()
    plt.cla()
    plt.close()
    #plt.show()
