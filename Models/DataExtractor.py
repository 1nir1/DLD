import csv
from Models.Point import Point

def ExtractPointsByArea(fileName, minArea, maxArea):
    points = []

    with open(fileName , newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            area = row['Area']
            xMid = row['XM']
            yMid = row['YM']
            feret = row['Feret']

            if  xMid != '' and  yMid != '' and feret != '' and area != '':
                floatArea = float(area)
                if floatArea >= minArea and floatArea <= maxArea:
                    point = Point(xMid, yMid, feret)
                    points.append(point)

    return points