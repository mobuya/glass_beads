# Bead Processing Tool for Archaeology

This tool contains functions for processing, measuring and analyzing bead images.

To use this tool it has to follow a specific format:
- the image HAS to have a resolution >= 6000 x 4000
- please make sure the brightness is equal throughout the whole image (darker exposure will not produce clean results)
- the image has to contain the following: a scale at the BOTTOM CENTER of the image, either 5 or 10 centimeters long
- the bead has to be within the image center
- the image name should always end with ```_VIEW``` (BEAD_ID_A, BEAD_ID_B1, etc.)

Example image: 

![RESIZED_MPULDF_009_001_B1](https://github.com/user-attachments/assets/f50806f4-41c0-4b7d-960c-32573b31bbbc)


## Main Features
- Calculates bead size and measurements based on contours.
- Places beads on canvases (single or multiple views).
- Extracts the dominant color of beads.
- Supports configuration for different image resolutions.
- Saves size calculations and color analysis in a xlsx file, within the output folder.


## Relevant libraries

* NumPy                     1.26.4
* OpenPyXL                  3.1.5
* OpenCV                    4.9.0

##  Installation

1. Clone the repository
2. Move to project directory
3. Set up virtual environment
    - ```python -m venv opencvenv```
4. Install OpenCV indside the environment (version in project 4.9.0)
    - ```pip install opencv-python==4.9.0```


## Usage


1. Place your images in the ```upload_images/```folder.
2. In the ```core.process_start```set the booleans for MERGE and TRANSPARENT to desired output.
3. Run ```python -m core.process_start```


The output of the images is then stored in ```processed_bead_output/``` folder where also the ```xlsx``` file can be found with the required bead data.

# IMPORTANT

In case issues occur within processing a bead, those will be stored in the folder ```beads_to_review```!

Each processing will create a ```processing.log```, in here you will find relevant information which bead could not be processed, wether the image resolution was invalid, or if the scale could not be detected causing the size measurements to be missing, etc.


## Testing

Unittest were only created for the key functions:

* config_manager
* find_object
* place_object
* pixel_per_metric
* size_calculation