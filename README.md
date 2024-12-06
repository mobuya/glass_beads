## About the Project

Work in progress for my thesis, consisting of three main parts:
 1. Bead segmentation: implemented segmenting single pearls, merge function missing
 2. Size prediction: works, but only when scale is valid on that picture, missing handling when scale invalid
 3. Web interface: not yet implemented

### Files for each task:
1. Segmentation:
     - ```enhance_threshold.py``` creates binary threshold image
     - ```find_object.py``` finds bead contour
     - ```place_object.py``` places object on transparent backgorund
     - ```segmentation.py``` combined the above functions, reads throug image paths to process multiple images at once
2. Size prediction:
   - ```pixel_per_metric.py``` calculates the pixel per metric based on the scale, uses threshold function from above too
   - ```size_calculation.py``` gets dimension of object with the help of ppm
   - ```prediction.py``` combines all functions into one

Helpers: 
  - ```id_parser.py``` saves the beads id and file name from image path
  - ```constants.py``` saves constant values that are based on image resolution
  - ```config_manager.py``` determines constant values based on image resolution

The ```process_start.py``` file combines the current progress of segmentation and size prediction, used for smoke tests to see current functionality.

Missing:
  - merging multiple views on one image
  - resolving the invalid scale problem
  - optimization with mask rescaling
  - unit test
  - segmentation validation
  - web interface
