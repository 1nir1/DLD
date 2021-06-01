# DLD
Dewetting Line Detector.
This project was created for identifying and analyzing line-patterns in a CSV file format input.

## Input
Each line in the CSV **input** describes a dot in 2D-space, those dots have a Feret diameter, X-center and Y-center. Input must be added to **Source** directory (if no such directory exist on you local computer, please create it).
A picture of valid CSV file for example - ![alt text](https://github.com/1nir1/DLD/blob/master/Doc/ValidCsvExample.jpeg "Valid CSV example")
The CSV file must include the following columns: 'Area', 'XM', 'YM', 'FERET'. Those are the only parts used in the final calculations. CSV input, missing at least one of those parts, will result a failure.

## Output
**The output** contains two parts - 
*Part I* - Command line output will describe the workflow while analyzing the sample - the workflow contains 4 steps:
  1. "Analyzing sample sample-name"
  2. "Done analyzing sample sample-name"
  3. "Saving results for sample sample-name"
  4. "Done saving results for sample sample-name"
*Part II* - In the "Dest" folder (Will be automatically created) you'll find the following data - a sub-folder named after the sample will be created (for our example here, it will be created under "./Dest/sample-name").
This folder will contain another sub folder, which will be named "outputX" (X will be the number of times you ran the project on the specific sample, this was done to avoid deleting previous results). In that folder you'll see two files "sample-name.pdf" and "sample-name.txt".
"sample-name.pdf" will be a picture of all the linear lines found in the sample. It should look something like this -
![alt text](https://github.com/1nir1/DLD/blob/master/Doc/sample-name.pdf.jpeg "Valid CSV example")
"sample-name.txt" will be a log describing all the lines found in the sample, which points it contains, and some general data about it. It should look something like this -
![alt text](https://github.com/1nir1/DLD/blob/master/Doc/sample-name.txt.jpeg "Valid CSV example")
## How to use this project?
Insert a CSV sample file into the "Source" folder (if it doesn't exist, please create it), open the CMD and run `python DLD.py --fileName=sample-name`.
For fine-tuning of the sample's parametre see the help section -
 ![alt text](https://github.com/1nir1/DLD/blob/master/Doc/HelpSection.jpeg "Valid CSV example")
