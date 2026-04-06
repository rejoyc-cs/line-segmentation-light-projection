# Generalized Line Segmentation for Multi-Script Handwritten Documents

This repository provides a **Python implementation** of the line
segmentation method proposed in the paper:

**Title:** *A generalized line segmentation method for multi-script
handwritten text documents*\
**Authors:** Payel Rakshit, Chayan Halder, Md Obaidullah Sk, Kaushik
Roy\
**Journal:** Expert Systems with Applications\
**DOI:** https://doi.org/10.1016/j.eswa.2022.118498

------------------------------------------------------------------------

## Overview

This repository contains a **Python implementation** of the line
segmentation algorithm proposed in the above paper.

The goal of the method is to segment handwritten document images into
individual text lines in a **script-independent manner**, making it
suitable for **multi-script handwritten documents**.

The implementation is intended primarily for **research and
experimentation**.\
It follows the methodology described in the paper but may not exactly
reproduce all implementation details used by the authors.

------------------------------------------------------------------------

## Pipeline Overview

The implementation follows the major stages described in the paper:

1.  **Pre-processing**
    -   Convert RGB image to grayscale
    -   Adaptive binarization
2.  **Light Projection Filling**
    -   Bi-directional projection used to separate text and non-text
        regions
3.  **Connected Component Analysis**
    -   Estimate average and median character height
4.  **Smoothing**
    -   Remove small gaps generated during light projection
5.  **Start Point Detection**
    -   Sliding window technique used to detect candidate text line
        locations
6.  **Boundary Tracking**
    -   Separators traced between adjacent text lines using boundary
        tracking
7.  **Line Extraction**
    -   Segmented text lines extracted and saved as individual images

------------------------------------------------------------------------

## Directory Structure

The repository expects the following directory structure:

project_root/ │ ├── main.py ├── Dataset/ │ ├── sample1.tif │ ├──
sample2.tif │ ├── sample3.tif │ └── ... │ └── lines/ ├── sample1/ │ ├──
filename_00.tif │ ├── filename_01.tif │ └── ... │ ├── sample2/ │ ├──
filename_00.tif │ └── ... │ └── ...

### Description

-   **main.py**\
    Python script implementing the full line segmentation pipeline.

-   **Dataset/**\
    Directory containing input handwritten document images.

-   **lines/**\
    Output directory automatically created by the program. Each document
    will have its own subfolder containing the extracted text line
    images.

------------------------------------------------------------------------

## How to Run the Code

### 1. Install Dependencies

The implementation requires the following Python packages:

-   opencv-python
-   numpy

Install them using:

pip install opencv-python numpy

------------------------------------------------------------------------

### 2. Prepare the Dataset

Place all handwritten document images inside the `Dataset/` directory.

Example:

Dataset/ doc1.tif doc2.tif doc3.tif

Supported formats typically include:

-   .tif
-   .png
-   .jpg

------------------------------------------------------------------------

### 3. Run the Program

Execute the script from the project root directory:

python main.py

------------------------------------------------------------------------

### 4. Output

After processing, segmented lines will be saved in the `lines/`
directory.

Example:

lines/ doc1/ filename_00.tif filename_01.tif filename_02.tif

Each output image corresponds to an **extracted text line** from the
original document.

------------------------------------------------------------------------

## Reference

If you use this implementation in your research, please cite the
original paper:

``` bibtex
@article{rakshit2023generalized,
  title={A generalized line segmentation method for multi-script handwritten text documents},
  author={Rakshit, Payel and Halder, Chayan and Sk, Md Obaidullah and Roy, Kaushik},
  journal={Expert Systems with Applications},
  volume={212},
  pages={118498},
  year={2023},
  publisher={Elsevier}
}
```

or

Rakshit, P., Halder, C., Sk, M. O., & Roy, K. (2023).\
*A generalized line segmentation method for multi-script handwritten
text documents*.\
**Expert Systems with Applications**, 212, 118498.

------------------------------------------------------------------------

## Disclaimer

This repository provides a **simplified and unofficial implementation**
of the algorithm.\
It is **not the official implementation released by the authors**.

The implementation is intended for **educational and research purposes
only**.
