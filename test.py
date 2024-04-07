# Notes
# https://www.geeksforgeeks.org/maximum-distance-between-two-points-in-coordinate-plane-using-rotating-calipers-method/
# https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/

# h5py file
import h5py
import numpy as np

# File management
import sys
import os

#Calculations
import math

# Dictionary to represent stored data
# Dictionary has files as keys, values of deviceDictionary that has key of devicename, value of avg or distance
# data has keys=filename, value=list<deviceDict>
# deviceDict has keys=device[sensor#], value=list<sensor avg> for avg
# deviceDict has keys=device[sensor#], value=maxDistance for distance
# Call addFile() method before calling addDeviceAvg() or addDeviceDistance()
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

# Object used to represent a 3d sample point
class SamplePoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

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
def compute(avgOutput, distOutput, inputFolder, outputFolder, fileList):
    # Loop through files in folder
    for file in fileList:
        filePath = inputFolder + '/' + file
        # Checks if file is a .hdf5 file
        if filePath.endswith('.hdf5'):
            fileH = h5py.File(filePath, 'r')
            deviceList = list(fileH.keys())
            avgOutput.addFile(file)
            distOutput.addFile(file)
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
                        computeMaxDistance(distOutput, sensorDataset, file, deviceName)

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

# Computes max euclidean distance in sampledataset and adds to distance dictionary
def computeMaxDistance(maxOutput, sensorDataset, filename, deviceName):
    sampleList = []
    for sample in sensorDataset:
        point = SamplePoint(sample[0], sample[1], sample[2])
        sampleList.append(point)
    
    maxOutput.addDeviceDistance(filename, deviceName, maxDistance(sampleList))

# Finds the max distance between 2 3d points in a list of points
# Brute force approach of O(n^2)
def maxDistance(sampleList):
    n = len(sampleList)
    maxDistance = 0
 
    # Iterate over all possible pairs
    for i in range(n):
        for j in range(i + 1, n):
             
            # Update maxm
            maxDistance = max(maxDistance, euclideanDistance(sampleList[i], sampleList[j]))
    return maxDistance

# Computes the max euclidean distance between 2 3d points
def euclideanDistance(sample1, sample2):
    x1, y1, z1 = sample1.x, sample1.y, sample1.z
    x2, y2, z2 = sample2.x, sample2.y, sample2.z
    squaredDistance = (x2 - x1)**2 + (y2-y1)**2 + (z2-z1)**2
    return math.sqrt(squaredDistance)



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
    compute(avgOutput, distOutput, inputFolder, outputFolder, fileList)
    print(avgOutput)
    print(distOutput)

if __name__ == "__main__":
    main()
