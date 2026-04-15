
import laspy
import numpy as np

print("Generating mock 3D Point Cloud...")

# Create a blank LAS file structure
header = laspy.LasHeader(point_format=3, version="1.2")
las = laspy.LasData(header)

# Generate 10,000 random X and Y coordinates
las.x = np.random.uniform(0, 100, 10000)
las.y = np.random.uniform(0, 100, 10000)

# Generate Z coordinates (Elevations)
# - 8,000 points of flat Ground (Elevation 10m to 12m)
# - 1,900 points of Trees/Buildings (Elevation 12m to 30m)
# - 100 points of floating Noise/Clouds (Elevation 80m to 100m)
las.z = np.concatenate([
    np.random.uniform(10, 12, 8000),
    np.random.uniform(12, 30, 1900),
    np.random.uniform(80, 100, 100)
])

# Save it to your folder
las.write("raw_flight_data.las")
print("Success! Created 'raw_flight_data.las' with 10,000 points.")