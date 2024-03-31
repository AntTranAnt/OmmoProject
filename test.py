import h5py
import numpy as np

# File management
import sys

def main():
    # Input validation for 2 folders
    if len(sys.argv) != 3:
        print("Format: python OmmoProject.py input_file output_file")
        return
    