import numpy as np
import cv2
import os

from utils import parse_filename_from_path, parse_bead_id_and_view
from canvas import place_obj_on_background
from processing import find_artifact_contour, get_horizontal_dimension, calculate_ppm, get_dominant_colors
from config import HOLE_VIEW, NO_HOLE_VIEW

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level


'''
In case an image can't be processed: no bead contour found, the scale could not be detected or if it the segmentation may not be clean,
all these get stored in the 'beads_to_review' folder, next to their ID the issue gets appended to the name.
'''

failed_beads_path = 'beads_to_review'
output_counter = 1

output_path = failed_beads_path
while os.path.exists(output_path):
        logger.info(f"A folder with the name {output_path} already exists, created new one appending {output_counter} to folder name.")
        output_path = failed_beads_path + f"_{output_counter}"
        output_counter += 1
os.makedirs(output_path) 


def process_bead_data(paths, config, merge, transparent, scale_size):
    '''
    Processes a list of image paths to segment, crop, and measure artifacts (beads) from images.  
    The function extracts contours, calculates object dimensions, and optionally merges multiple views into a single image.

    Parameters
    ----------
    paths : list of str
        A list of file paths to the input images.

    config : dict
        Configuration object containing parameters for image processing.

    merge : bool
        If True, all processed artifacts are combined into a single output image.  
        If False, each artifact is processed and saved individually.

    transparent : bool
        Determines if the background of output image should be transparent, if set to False the background is white.

    scale_size : float
        The physical size (in mm/cm) of the scale in the image, used for object measurement.

    Returns
    -------
    processed_images : dict
        A dictionary where keys are image identifiers (bead_id) and values are the processed (segmented) images.

    final_object_length : float
        The average length (in mm) of pearls from view A. Returns 0.0 if no measurements are available.

    final_object_width : float
        The average width (in mm) of pearls from view B. Returns 0.0 if no measurements are available.

    dom_color : numpy.ndarray or None
        The dominant colors extracted from pearls in view A as an RGB array.  
        Returns None if no colors were extracted.

    Notes
    -----
    - View A images are used for length and color extraction, while view B images are used for width measurements.  
    - Missing contours or failed scale detection will log warnings and skip the affected images.  
    '''  
    processed_images = {}
    length_viewA = []
    width_viewB = []

    out_contours = []
    in_contours = []
    images = []

    for path in paths:
        bead_id, full_bead_view =  parse_bead_id_and_view(parse_filename_from_path(path))
        bead_view = NO_HOLE_VIEW if "A" in full_bead_view else HOLE_VIEW
        
        original_image = cv2.imread(path)

        if original_image is None:
            logger.warning(f"The needed image could not be opened: {path}, so the bead {bead_id} had to be skipped")
            continue

        ppm = calculate_ppm(original_image, scale_size, config)

        artifact_contour, inner_contour, clahe_bool = find_artifact_contour(original_image, bead_view, config) 
        
        # in case CLAHE is applied, save that bead since the output may not be clean
        if clahe_bool:
            output_image_path = os.path.join(failed_beads_path, f"{bead_id}_{full_bead_view}_SIMILAR_TO_BACKGROUND.png")
            cv2.imwrite(output_image_path, original_image)
    
        if artifact_contour is None:
            output_image_path = os.path.join(failed_beads_path, f"{bead_id}_{full_bead_view}_NO_BEAD_CONTOUR.png")
            cv2.imwrite(output_image_path, original_image)
            logger.info(f"I M P O R T A N T: The image of bead {bead_id} ({bead_view}) could NOT find a valid contour! PLEASE save this info and manually edit bead; further bead processing could not continue.")
            continue
        

        if ppm is None:
            output_image_path = os.path.join(failed_beads_path, f"{bead_id}_{full_bead_view}_INVALID_SCALE.png")
            cv2.imwrite(output_image_path, original_image)
            logger.info(f"For bead {bead_id}, view {bead_view} the ppm ratio could not be calculated; thus no valid size calculation.")
            object_width = 0.0
        else:
            object_width = get_horizontal_dimension(artifact_contour, ppm, config)


        if object_width != 0.0:
            if bead_view == NO_HOLE_VIEW:
                length_viewA.append(object_width)
            else:
                width_viewB.append(object_width)

        images.append(original_image)
        out_contours.append(artifact_contour) 
        in_contours.append(inner_contour)      

        if merge:
            output_file = bead_id
        else:
            output_file = parse_filename_from_path(path)
            canvas = place_obj_on_background([original_image], [artifact_contour], [inner_contour], transparent, config)
            processed_images[output_file] = canvas

    if merge: 
        canvas = place_obj_on_background(images, out_contours, in_contours, transparent, config)
        processed_images[output_file] = canvas


    dom_colors = get_dominant_colors(images, out_contours, in_contours)
    final_object_length = round(sum(length_viewA) / len(length_viewA), 1) if length_viewA else 0.0
    final_object_width = round(sum(width_viewB) / len(width_viewB), 1) if width_viewB else 0.0

    return processed_images, final_object_length, final_object_width, dom_colors
