import csv
import matplotlib.pyplot as plt

def DoesPointsCollide(point1, point2):
    doesXCollide = True # point1._x + point1._radius >= point2._x - point2._radius or point1._x - point1._radius <= point2._x + point2._radius
    doesYCollide = point1._y + point1._radius <= point2._y - point2._radius or point1._y - point1._radius >= point2._y + point2._radius

    return doesXCollide and doesYCollide


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
        self._smalletYPoint = None
        self._biggestYPoint = None

    def TryToAddPoint(self, point):
        if len(self._points) == 0:
            self._points.append(point)
            self._biggestYPoint = point
            self._smalletYPoint = point
            return True
        
        if point._y - point._radius <= self._biggestYPoint._y + self._biggestYPoint._radius and point._y + point._radius >= self._biggestYPoint._y - self._biggestYPoint._radius \
        or point._y + point._radius >= self._smalletYPoint._y - point._radius and point._y - point._radius <= self._smalletYPoint._y + point._radius:
            self._points.append(point)
            if point._y + point._radius > self._biggestYPoint._y + self._biggestYPoint._radius:
                self._biggestYPoint = point
            if point._y - point._radius < self._smalletYPoint._y + self._smalletYPoint._radius:
                self._smalletYPoint = point
            return True
        # if DoesPointsCollide(point, self._smalletYPoint) or DoesPointsCollide(point, self._biggestYPoint):
        #     self._points.append(point)
        #     if(point._y + point._radius > self._biggestYPoint._y + self._biggestYPoint._radius):
        #         self._biggestYPoint = point
        #     if(point._y - point._radius < self._smalletYPoint._y - self._smalletYPoint._radius):
        #         self._smalletYPoint = point
        #     return True
        
        return False
    
    def GetCoordiantes(self):
        outputX = []
        outputY = []
        for point in self._points:
            outputX.append(point._x)
            outputY.append(point._y)

        return (outputX, outputY)

points = []
with open('Results.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        xMid = row['XM']
        yMid = row['YM']
        feret = row['Feret']
        if  xMid != '' and  yMid != '' and feret != '':
            point = Point(xMid, yMid, feret)
            print(point)
            points.append(point)
            # xPoints.append(row['XM'])
            # yPoints.append(row['YM'])

print("--------------- sorted -------------")
points.sort(key=lambda point: point._x)
print(points)
print("---------done----------")

lines = []
i = 0
for point in points:
    foundLine = False
    for line in lines:
        if(line.TryToAddPoint(point)):
            print("{0} found line".format(point))
            foundLine = True
            break
    
    if foundLine is False:
        print("{0} started new line".format(point))
        line = Line()
        line.TryToAddPoint(point)
        lines.append(line)

with open('out.txt', 'w') as f:
    for line in lines:
        (xCoordinates, yCoordinatess) = line.GetCoordiantes()
        plt.plot(xCoordinates, yCoordinatess)

        print("new line", file=f)
        print(line._points, file=f)

plt.show()
#print("{0} {1}".format(points[1], points[2]))

# print("xPoints {0}".format(xPoints))
# print("yPoints {0}".format(yPoints))

# yPoints.sort(key = float)
# print("sorted yPoints {0}".format(yPoints))
