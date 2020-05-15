import argparse

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