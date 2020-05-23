import os
import itertools
from pathlib import Path
import matplotlib.pyplot as plt

from Models.Point import Point
from Models.Line import Line
from Models.DataExtractor import ExtractPointsByArea

def _uniqueFile(basename, ext):
    actualname = "%s.%s" % (basename, ext)
    c = itertools.count()
    while os.path.exists(actualname):
        actualname = "%s (%d).%s" % (basename, next(c), ext)
    return actualname

def _movingWindow(n, iterable):
  start, stop = 0, n
  while stop <= len(iterable):
      yield iterable[start:stop]
      start += 1
      stop += 1

def _mergeCloseLines(lines):
    wereLinesMerged = True
    while wereLinesMerged:
        linesAfterMerge = []
        # we sort by the average y point, becuase it is a "blocking-factor" if line1 and line3 have line2 btw them, they cannot be merged!
        lines.sort(key=lambda line: line.GetAverageYPoint())
        wereLinesMerged = False
        for coupleOflines in _movingWindow(2, lines):
            if Line.CanLinesBeMerged(coupleOflines[0], coupleOflines[1]):
                linesAfterMerge.append(coupleOflines[0] + coupleOflines[1])
                lines.remove(coupleOflines[0])
                lines.remove(coupleOflines[1])
                wereLinesMerged = True
        lines = lines + linesAfterMerge
    
    return lines

def _filterSingleDots(lines):
    filteredLines = [line for line in lines if line.Size() > 1]
    return filteredLines

def _createLinesFromPoints(points):
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

    return lines

class Sample:
    def __init__(self, fileName, minArea, maxArea, deltaXFactor):
        self._points = []
        self._lines = []

        baseFileName = os.path.splitext(fileName)[0]
        self._baseFileName = baseFileName
        self._sourceFile = "Source/{0}.csv".format(self._baseFileName)

        destPath = "Dest/{0}".format(self._baseFileName)
        Path(destPath).mkdir(parents=True, exist_ok=True)
        self._destFileName = "{0}/{1}".format(destPath, self._baseFileName)

        self._minArea = minArea
        self._maxArea = maxArea
        self._deltaXFactor = deltaXFactor

    def Analyze(self, saveLog):
        print("Analyzing sample {0}".format(self._baseFileName))

        self._points = ExtractPointsByArea(self._sourceFile, self._minArea, self._maxArea)
        self._points.sort(key=lambda point: point.x)
        deltaX = self._points[-1].x - self._points[0].x

        lines = _createLinesFromPoints(self._points)
        lines = _mergeCloseLines(lines)
        lines = _filterSingleDots(lines)

        with open(_uniqueFile(self._destFileName,"txt"), 'w') as f:
            for index,line in enumerate(lines):
                linearReprLine = line.GetLinearReprLine()
                lineLength = linearReprLine.GetLineLength()

                if lineLength < self._deltaXFactor * deltaX:
                    continue
                
                (x, y) = line.GetCoordiantes()
                plt.plot(x,y, label="{0} raw".format(index))
                (linearX, linearY) = linearReprLine.GetCoordiantes()
                plt.plot(linearX, linearY, '-', label="{0} linear".format(index))

                print("raw line index:{0}, {1}".format(index, line), file=f)
                print(line.points, file=f)
                
                print("linear line index:{0}, {1}".format(index, linearReprLine), file=f)
                print(linearReprLine.points, file=f)

                line.FilterOutFarPoints(linearReprLine)
                print("afterFilteartion line index:{0}, {1}".format(index, line), file=f)
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

        plt.savefig(_uniqueFile(self._destFileName, "pdf"))
        plt.clf()
        plt.cla()
        plt.close()

        print("Done analyzing sample {0}".format(self._baseFileName))
    
    def SaveResults(self):
        print("Saving results for sample {0}".format(self._baseFileName))
        print("Done saving results for sample {0}".format(self._baseFileName))
        print("")
