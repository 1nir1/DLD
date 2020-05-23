from Models.Sample import Sample
from Models.IO import GetCommandLineParams

if __name__ == "__main__":
    ######
    saveLog = True
    ######

    (fileNames, minArea, maxArea, deltaXFactor) = GetCommandLineParams()

    for fileName in fileNames:
        sample = Sample(fileName, minArea, maxArea, deltaXFactor)
        sample.Analyze(saveLog)
        sample.SaveResults()
