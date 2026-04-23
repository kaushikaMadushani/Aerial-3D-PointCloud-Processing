# 3D LiDAR Point Cloud Processing Pipeline

## Overview
This repository contains a custom Python-based pipeline for ingesting, filtering, and classifying high-resolution aerial LiDAR data. It is designed to process compressed `.laz` files, remove atmospheric/sensor noise, and classify bare-earth ground points using ASPRS standards.

## Tech Stack
* **Language:** Python
* **Libraries:** `laspy[lazrs]`, `numpy`, `time`
* **Visualization:** QGIS (3D Map Views, Elevation/Z-Ramping, ASPRS Classification Symbology)
* **Data Source:** OpenTopography (LINZ / New Zealand High-Resolution Terrain Data)

## Pipeline Features
1. **Data Ingestion:** Reads millions of raw points from highly compressed LAZ formats.
2. **Statistical QA/QC Noise Removal:** Calculates global Z-mean and standard deviation to automatically filter out high-Z outliers (e.g., sensor errors, birds, cloud reflections).
3. **ASPRS Ground Classification:** Implements a global-minimum thresholding algorithm to isolate bare-earth points (Class 2) from unclassified structures and vegetation (Class 1).
4. **Data Export:** Repackages the classified array into a clean `.laz` file with intact CRS/GPS coordinates for accurate GIS rendering.

## Future Improvements
* Integration of a Progressive Morphological Filter (PMF) or PDAL to improve ground classification accuracy on highly sloped/hilly terrain.
