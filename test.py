# Notes
# https://www.geeksforgeeks.org/maximum-distance-between-two-points-in-coordinate-plane-using-rotating-calipers-method/
# https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/

# h5py file
import h5py
import numpy as np

# File management
import sys
import os

# Dictionary to represent stored data
# data has keys=filename, value=list<deviceDict>
# deviceDict has keys=device[sensor#], value=list<sensor avg> for avg
# deviceDict has keys=device[sensor#], value=maxDistance for distance
class OutputDictionary:
    def __init__(self):
        self.data = {}
    
    def addFile(self, filename):
        self.data[filename] = []
    
    def addDeviceAvg(self, filename, deviceName, avgList):
        deviceDict = {deviceName: avgList}
        self.data[filename].append(deviceDict)

    def addDeviceDistance(self, filename, deviceName, maxDistance):
        deviceDict = {deviceName: maxDistance}
        self.data[filename].append(deviceDict)
    
    def __str__(self):
        return str(self.data)

# Checks if argument is valid with input folder and output folder
# returns list of files if valid
# returns empty list if not
def inputValidation(inputFolder, outputFolder) -> list:
    # Checks if folders exists
    if not os.path.exists(inputFolder):
        print("Input folder does not exist")
        return []
    elif not os.path.exists(outputFolder):
        print("Output folder does not exist")
        return []
    
    # Checks if input folder is empty
    fileList = os.listdir(inputFolder)
    if len(fileList) == 0:
        print("Input folder is empty")
        return []
    
    return fileList

# Loops through all files and finds sensor dataset from all valid 'Position' datasets
# file.hdf5 -> list<devices> -> device -> list<datasets> -> position dataset -> sensor dataset
def compute(avgOutput, inputFolder, outputFolder, fileList):
    output = dict() #key = file name, maps to list of x, y, z data
    # Loop through files in folder
    for file in fileList:
        filePath = inputFolder + '/' + file
        # Checks if file is a .hdf5 file
        if filePath.endswith('.hdf5'):
            fileH = h5py.File(filePath, 'r')
            deviceList = list(fileH.keys())
            avgOutput.addFile(file)
            # Loops through device groups in file
            for device in deviceList:
                # Checks if device has Position dataset
                tempDevice = fileH[device]
                if 'Position' in tempDevice:
                    positionDataset = tempDevice['Position']
                    shape = positionDataset.shape
                    # Loops through each sensor in the device
                    sensorIndex = 1
                    for i in range(shape[sensorIndex]):
                        sensorDataset = positionDataset[:, i, :]
                        deviceName = device + "[" + str(i) + "]"
                        computeAvgPosition(avgOutput, sensorDataset, file, deviceName)

# Computes the average position for each sensorDataset and inputs to output dictionary
def computeAvgPosition(avgOutput, sensorDataset, filename, deviceName):
    sampleNum = 0
    xSum = 0
    ySum = 0
    zSum = 0
    for sample in sensorDataset:
        sampleNum += 1
        xSum += sample[0]
        ySum += sample[1]
        zSum += sample[2]
    
    # Checks if sample is empty, if not then append results to avgOutput
    if sampleNum != 0:
        xSum /= sampleNum
        ySum /= sampleNum
        zSum /= sampleNum
        avgOutput.addDeviceAvg(filename, deviceName, [xSum, ySum, zSum])

def main():
    # Checks for proper input
    if len(sys.argv) != 3:
        print("Format: python OmmoProject.py input_folder output_folder")
    inputFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    fileList = inputValidation(inputFolder, outputFolder)
    if len(fileList) == 0: return

    # Dictionary to keep track of results
    avgOutput = OutputDictionary()
    distOutput = OutputDictionary()
    compute(avgOutput, inputFolder, outputFolder, fileList)
    print(avgOutput)

if __name__ == "__main__":
    main()
