# Notes
# https://www.geeksforgeeks.org/maximum-distance-between-two-points-in-coordinate-plane-using-rotating-calipers-method/
# https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/

# h5py file
import h5py
import numpy as np

# File management
import sys
import os

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

# Computes the average position for each sensor on each device in all valid files
def computeAveragePosition(inputFolder, outputFolder, fileList):
    output = dict() #key = file name, maps to list of x, y, z data
    for file in fileList:
        filePath = inputFolder + '/' + file
        if filePath.endswith('.hdf5'):
            file = h5py.File(filePath, 'r')
            deviceList = list(file.keys)


def main():
    # Checks for proper input
    if len(sys.argv) != 3:
        print("Format: python OmmoProject.py input_folder output_folder")
    inputFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    fileList = inputValidation(inputFolder, outputFolder)
    if len(fileList) == 0: return

    computeAveragePosition(inputFolder, outputFolder, fileList)

    # f = h5py.File('1.hdf5', 'r')
    # # List of device groups
    # deviceList = list(f.keys())
    # print(deviceList)
    # # Device 1
    # device = f[deviceList[0]]
    # print(device)
    # # Position dataset of device 1
    # dataset = device['Position']
    # print(dataset)
    # # Dataset of sample 1 of device 1
    # sample1Dataset = dataset[:, 0, :]
    # print(sample1Dataset)
    # for sample in sample1Dataset:
    #     print(sample[0])
    #     print(sample[1])
    #     print(sample[2])

if __name__ == "__main__":
    main()
