# h5py file
import h5py
import numpy as np

# File management
import sys
import os

# Checks if argument is valid with input folder and output folder
# returns true if proper input validation
def inputValidation() -> bool:
    # Checks for proper input
    if len(sys.argv) != 3:
        print("Format: python OmmoProject.py input_folder output_folder")
        return False
    
    inputFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    
    # Checks if folders exists
    if not os.path.exists(inputFolder):
        print("Input folder does not exist")
        return False
    elif not os.path.exists(outputFolder):
        print("Output folder does not exist")
        return False
    
    # Checks if input folder has data
    if len(os.listdir(inputFolder)) == 0:
        print("Input folder is empty")
        return False
    
    return True

def main():
    # Input validation for 2 folders
    if not inputValidation(): return
    
    f = h5py.File('1.hdf5', 'r')
    print(list(f.keys()))
    dset = f['Device_792888129_0']

if __name__ == "__main__":
    main()
