import laspy
import numpy as np
import time

def process_real_lidar(input_file, output_file):
    start_time = time.time()
    print(f"--- Starting Production Pipeline ---")
    
    # 1. INGESTION
    print(f"Step 1: Reading compressed LiDAR data: {input_file}...")
    las = laspy.read(input_file)
    original_count = len(las.points)
    print(f"Successfully loaded {original_count:,} raw points.")

    # 2. QA/QC NOISE REMOVAL
    print("\nStep 2: Running Statistical Noise Filter...")
    z_mean = np.mean(las.z)
    z_std = np.std(las.z)
    
    # Drop points higher than 3 standard deviations
    valid_mask = (las.z < (z_mean + 3 * z_std))
    
    # THE FIX: Apply the mask directly to the original file to keep the GPS Map Coordinates!
    las.points = las.points[valid_mask]
    
    noise_removed = original_count - len(las.points)
    print(f"Detected and deleted {noise_removed:,} floating noise points.")

    # 3. GROUND CLASSIFICATION (ASPRS)
    print("\nStep 3: Classifying Ground vs. Non-Ground (ASPRS Standard)...")
    z_min = np.min(las.z)
    ground_threshold = z_min + 1.5  
    
    las.classification[las.z <= ground_threshold] = 2 # ASPRS Ground
    las.classification[las.z > ground_threshold] = 1  # ASPRS Unclassified/Structures
    
    ground_points = np.sum(las.classification == 2)
    print(f"Classified {ground_points:,} points as Bare-Earth Ground.")

    # 4. EXPORT
    print(f"\nStep 4: Exporting clean model...")
    las.write(output_file)
    
    end_time = time.time()
    print(f"Pipeline Complete! Processed in {round(end_time - start_time, 2)} seconds.")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    RAW_FILE = "real_data.laz" 
    CLEAN_FILE = "clean_real_data.laz" 
    
    process_real_lidar(RAW_FILE, CLEAN_FILE)