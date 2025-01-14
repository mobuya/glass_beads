## About the Project

OpenCV version: 4.9.0

Work in progress for my thesis, consisting of three main parts:
 1. Bead segmentation: implemented
 2. Size prediction: implemented
 3. Web interface: not yet implemented

### Files for each task:
1. Segmentation:
     - ```enhance_threshold.py``` creates binary threshold image
     - ```find_object.py``` finds bead contour
     - ```place_object.py``` places object(s) on transparent or white background

2. Size prediction:
   - ```pixel_per_metric.py``` calculates the pixel per metric based on the scale, uses threshold function from above too
   - ```size_calculation.py``` gets dimension of object with the help of ppm

```crop_and_measure.py``` combined all the above into one

3. Color extraction: not yet done the way it should be, work in progress
    -```crop_and_extraction.py``` with kmeans determines 3 main colors of bead

Helpers: 
  - ```id_parser.py``` saves the beads id and file name from image path
  - ```constants.py``` saves constant values that are based on image resolution
  - ```config_manager.py``` determines constant values based on image resolution
  - ```color_converter.py``` converts color values for XLSX file

The ```process_start.py``` file combines the current progress of segmentation and size prediction, used for smoke tests to see current functionality.

Missing:
  - color extraction PER bead view
  - unit test
  - segmentation validation (will be done in different project)
  - web interface
