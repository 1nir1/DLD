import argparse

def GetCommandLineParams():
    parser=argparse.ArgumentParser(description='DewettingLineDetector')
    parser.add_argument('--fileName', nargs=1, type=str, default=None, help='The path for the csv source file')
    parser.add_argument('--minArea', type=float, default=0, help='Minimum area for circles - smaller circles will be filtered out. Default value is 0')
    parser.add_argument('--maxArea', type=float, default=float("inf"), help='Maximum area for circles - bigger circles will be filtered out. Default value is infinity')
    parser.add_argument('--deltaXFactor', type=float, default=0.7, help='Factor to multiply the deltaX of the sample with - lines below that deltaX * factor length, will be filtered out')
    args=parser.parse_args()

    fileName = args.fileName
    fileName = "Source/" + fileName[0].replace("'","")
    minArea = args.minArea
    maxArea = args.maxArea
    deltaXFactor = args.deltaXFactor

    return (fileName, minArea, maxArea, deltaXFactor)