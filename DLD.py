from Models.Sample import Sample
from Models.IO import GetCommandLineParams

if __name__ == "__main__":
    (fileNames, minArea, maxArea, deltaXFactor) = GetCommandLineParams()

    for fileName in fileNames:
        try:
            sample = Sample(fileName, minArea, maxArea, deltaXFactor)
            sample.Analyze()
            sample.SaveResults()
        except Exception as e:
            print(e)
