import laspy
import numpy as np

def clean_and_classify(input_file, output_file):
    print(f"--- Starting Pipeline ---")
    print(f"Step 1: Ingesting {input_file}...")
    las = laspy.read(input_file)
    original_count = len(las.points)
    print(f"Loaded {original_count} raw points.")

    print("\nStep 2: QA/QC Noise Removal...")
    # Calculate the average height and the standard deviation
    z_mean = np.mean(las.z)
    z_std = np.std(las.z)
    
    # Filter: Keep only points that are NOT crazy high up in the sky
    # (Filtering out anything higher than 3 standard deviations from the average)
    valid_mask = (las.z < (z_mean + 3 * z_std))
    
    # Create a clean dataset with only the valid points
    clean_las = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
    clean_las.points = las.points[valid_mask]
    
    noise_removed = original_count - len(clean_las.points)
    print(f"Detected and deleted {noise_removed} floating noise points.")

    print("\nStep 3: Ground Classification (ASPRS Standard)...")
    # Find the lowest point, and assume anything slightly above it is Ground
    z_min = np.min(clean_las.z)
    ground_threshold = z_min + 2.0  # Anything within 2 meters of the lowest point is ground
    
    # Apply ASPRS Codes: 2 = Ground, 1 = Unclassified (Trees/Buildings)
    clean_las.classification[clean_las.z <= ground_threshold] = 2
    clean_las.classification[clean_las.z > ground_threshold] = 1 
    
    ground_points = np.sum(clean_las.classification == 2)
    print(f"Classified {ground_points} points as bare-earth Ground.")

    print(f"\nStep 4: Exporting...")
    clean_las.write(output_file)
    print(f"Pipeline Complete! Cleaned model saved to: {output_file}")

if __name__ == "__main__":
    RAW = "raw_flight_data.las"
    CLEAN = "clean_ground_model.las"
    clean_and_classify(RAW, CLEAN)