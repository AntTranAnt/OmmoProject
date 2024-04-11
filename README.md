Project designed for Ommo Challenge Project

Instructions:
- Download Python
- Download h5py

Run:
Windows: python OmmoProject.py input_folder_path output_folder_path
Mac: python3 OmmoProject.py input_folder_path output_folder_path

OmmoProject.py reads in valid .hdf5 files from input folder, and computes average position and max distance into output folder. Designed for datasets from Ommo instruments, mainly datasets with 'Position' of shape (x, y, 3), with x = sampleNum, y = sensorNum.

Compute average position is O(N)

Compute distance is O(N^2)

Future Improvements:
Compute distance algorithm can be sped up to O(n log n) by using the rotating calipers method (adjusted for 3d points)