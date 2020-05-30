import os
import itertools
from pathlib import Path
import matplotlib.pyplot as plt
import Models.Consts

from Models.Point import Point
from Models.Line import Line
from Models.DataExtractor import ExtractPointsByArea

def _uniqueFolder(prefix):
    actualname = "%s/output" % (prefix)
    c = itertools.count()
    while os.path.exists(actualname):
        actualname = "%s/output%d" % (prefix, next(c))
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

def _getAverageNumberOfPointsPerLine(lines):
    averageNumberOfPointsPerLine = sum([len(line.points) for line in lines]) / len(lines)
    averageNumberOfPointsPerLineRounded = round(averageNumberOfPointsPerLine, Models.Consts.ROUNDED_DIGITS_NUMBER)
    return averageNumberOfPointsPerLineRounded

def _getLinesWithSufficientNumberOfPoints(lines):
    averageNumberOfPointsPerLine = _getAverageNumberOfPointsPerLine(lines)
    linesWithSufficientNumberOfPoints = [line for line in lines if len(line.points) > Models.Consts.AVERAGE_NUMBER_OF_POINTS_FACTOR * averageNumberOfPointsPerLine]
    return linesWithSufficientNumberOfPoints

def _configureAndSavePlot(destPath):
    ax=plt.gca()
    ax.xaxis.tick_top() 
    ax.invert_yaxis()
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 6})

    plt.savefig("{0}_graph.pdf".format(destPath))
    plt.clf()
    plt.cla()
    plt.close()

def _logLine(line, extraText, logFile):
    (x, y) = line.GetCoordiantes()
    plt.plot(x,y, label=extraText)
    print("{0} - {1}".format(extraText, line), file=logFile)
    print(line.points, file=logFile)

class Sample:
    def __init__(self, fileName, minArea, maxArea, deltaXFactor):
        self._points = []
        self._lines = []
        self._linesWithSufficientNumberOfPoints = []

        baseFileName = os.path.splitext(fileName)[0]
        self._baseFileName = baseFileName
        self._sourceFile = "Source/{0}.csv".format(self._baseFileName)

        destPathPrefix = "Dest/{0}".format(self._baseFileName)
        destPath = _uniqueFolder(destPathPrefix)
        Path(destPath).mkdir(parents=True, exist_ok=True)
        self._destFileName = "{0}/{1}".format(destPath, self._baseFileName)

        self._minArea = minArea
        self._maxArea = maxArea
        self._deltaXFactor = deltaXFactor

    def Analyze(self):
        print("Analyzing sample {0}".format(self._baseFileName))

        self._points = ExtractPointsByArea(self._sourceFile, self._minArea, self._maxArea)
        self._points.sort(key=lambda point: point.x)

        deltaX = self._points[-1].x - self._points[0].x

        lines = _createLinesFromPoints(self._points)
        lines = _mergeCloseLines(lines)
        lines = _filterSingleDots(lines)
        
        with open("{0}_log.txt".format(self._destFileName), 'w') as f:
            for index,line in enumerate(lines):
                _logLine(line, "{0} raw".format(index), f)

                linearReprLine = line.GetLinearReprLine()
                lineLength = linearReprLine.GetLineLength()
                if lineLength < self._deltaXFactor * deltaX:
                    continue
                
                _logLine(linearReprLine, "{0} linear".format(index), f)

                line.FilterOutFarPoints(linearReprLine)
                _logLine(line, "{0} after filteration".format(index), f)

                self._lines.append(line)

        _configureAndSavePlot(self._destFileName)

        self._linesWithSufficientNumberOfPoints = _getLinesWithSufficientNumberOfPoints(self._lines)

        print("Done analyzing sample {0}".format(self._baseFileName))
    
    def SaveResults(self):
        print("Saving results for sample {0}".format(self._baseFileName))
        numberOfPoints = len(self._points)
        numberOfGoodPoints = sum([len(line.points) for line in self._linesWithSufficientNumberOfPoints])
        orderFactor = numberOfGoodPoints / numberOfPoints
        
        averageNumberOfPointsPerRow = _getAverageNumberOfPointsPerLine(self._linesWithSufficientNumberOfPoints)

        print("numberOfGoodPoints: {0}, numberOfPoints: {1}, orderFactor: {2} averageNumberOfPointsPerRow: {3}".format(numberOfGoodPoints, numberOfPoints, orderFactor, averageNumberOfPointsPerRow))
        print("Done saving results for sample {0}".format(self._baseFileName))
        print("")
