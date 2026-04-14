"""
Automated 3D Point Cloud Processing Pipeline
Author: Kaushika Madushani
Description: This script ingests raw aerial photogrammetry/LiDAR point clouds (.las), 
performs QA/QC noise removal, and classifies ground points for 3D DTM generation.
"""

import laspy
import numpy as np

def clean_and_classify_pointcloud(input_path, output_path):
    print(f"Step 1: Ingesting raw aerial point cloud: {input_path}")
    # Load the raw 3D point cloud data
    las = laspy.read(input_path)
    
    print("Step 2: Performing QA/QC Noise Removal...")
    # Calculate the average height (Z-value) and standard deviation
    z_mean = np.mean(las.z)
    z_std = np.std(las.z)
    
    # Filter: Remove sensor errors (points way below ground) and atmospheric noise (birds/clouds)
    # We keep only points within 3 standard deviations of the mean elevation
    valid_points_mask = (las.z > (z_mean - 3 * z_std)) & (las.z < (z_mean + 3 * z_std))
    
    # Create a new, clean dataset
    clean_las = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
    clean_las.points = las.points[valid_points_mask]
    print(f"Removed {len(las.points) - len(clean_las.points)} noise points.")

    print("Step 3: Classifying Ground Points (ASPRS Standard)...")
    # Note: For complex terrain, I would integrate PDAL's Simple Morphological Filter (SMRF).
    # For this baseline, we establish a dynamic ground threshold based on local Z-minimums.
    z_min = np.min(clean_las.z)
    ground_threshold = z_min + (z_std * 0.25) 
    
    # Standard ASPRS Codes: 2 = Ground, 1 = Unclassified (Trees/Buildings)
    clean_las.classification[clean_las.z <= ground_threshold] = 2
    clean_las.classification[clean_las.z > ground_threshold] = 1 
    
    print(f"Step 4: Exporting clean, classified 3D model to {output_path}")
    clean_las.write(output_path)
    print("Pipeline Complete. Ready for DTM Rasterization.")

if __name__ == "__main__":
    # Define file paths (Variables ready for batch processing loop)
    RAW_DATA = "data/raw_flight_strip_01.las"
    PROCESSED_DATA = "results/clean_ground_model_01.las"
    
    # Execute pipeline
    # clean_and_classify_pointcloud(RAW_DATA, PROCESSED_DATA)