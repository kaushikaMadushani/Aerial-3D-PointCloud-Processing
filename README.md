Automated 3D Point Cloud Processing Pipeline
Overview
This repository contains a Python-based spatial pipeline designed to ingest, clean, and classify raw 3D point cloud data (.las/.laz) generated from aerial photogrammetry or LiDAR surveys. The goal is to automate the heavy lifting required before generating 3D Digital Terrain Models (DTMs).

The Tech Stack

Python 3: Core processing language.

laspy & numpy: Used for high-speed binary parsing of million-point datasets and vectorized statistical math.

Standardization: Strictly utilizes ASPRS (American Society for Photogrammetry and Remote Sensing) classification codes.

Pipeline Architecture:

High-Volume Ingestion: Parses massive .las flight strips.

QA/QC Noise Removal: Uses a Z-value statistical standard deviation mask to automatically detect and delete floating noise (clouds, birds) and sensor low-point errors.

Ground Classification: Separates bare-earth "Ground" points (ASPRS Code 2) from "Non-Ground" structures/vegetation (ASPRS Code 1) to prepare the data for bare-earth 3D rasterization.

Scalability: Designed to be wrapped in a for-loop to batch-process entire directories of aerial flight data simultaneously.
