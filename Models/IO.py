import argparse
from os import listdir
from os.path import isfile, join

def GetCommandLineParams():
    parser=argparse.ArgumentParser(description='DewettingLineDetector')
    parser.add_argument('--fileName', nargs=1, type=str, default=None, help='The path for the csv source file')
    parser.add_argument('--minArea', type=float, default=0, help='Minimum area for circles - smaller circles will be filtered out. Default value is 0')
    parser.add_argument('--maxArea', type=float, default=float("inf"), help='Maximum area for circles - bigger circles will be filtered out. Default value is infinity')
    parser.add_argument('--deltaXFactor', type=float, default=0.7, help='Factor to multiply the deltaX of the sample with - lines below that deltaX * factor length, will be filtered out')
    args=parser.parse_args()

    fileNames = args.fileName
    if fileNames is None:
        fileNames = [f for f in listdir('Source') if isfile(join('Source', f))]
    fileNames[:] = [ fileName.replace("'","") for fileName in fileNames ]
    minArea = args.minArea
    maxArea = args.maxArea
    deltaXFactor = args.deltaXFactor

    return (fileNames, minArea, maxArea, deltaXFactor)