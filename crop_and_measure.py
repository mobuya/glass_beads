import numpy as np
import cv2
from id_parser import parse_filename_from_path, parse_bead_id_and_view
from place_object import place_obj_on_background
from find_object import find_artifact_contour
from size_calculation import get_horizontal_dimension
from pixel_per_metric import calculate_ppm
from color_extraction import get_dominant_color



def crop_artifact_and_measure(paths, config, merge, transparent, scale_size):
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
    - If `merge` is enabled, all artifacts are placed on a single background; otherwise, they are saved separately.  
    - Missing contours or failed scale detection will log warnings and skip the affected images.  
    - Dominant colors are only extracted from view A due to the hole in view B pearls. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TODO: change this
    '''  
    processed_images = {}
    length_viewA = []
    width_viewB = []
    all_dom_colors = []

    out_contours = []
    in_contours = []
    images = []

    for path in paths:
        pearl_id, pearl_view =  parse_bead_id_and_view(parse_filename_from_path(path))
        pearl_view = 'A' if "A" in pearl_view else 'B'
        
        original_image = cv2.imread(path)

        ppm = calculate_ppm(original_image, scale_size, config)

        artifact_contour, inner_contour = find_artifact_contour(original_image, pearl_view, config) 
    
        if artifact_contour is None:
            # TODO: Error handling, logging
            print(f"For image no artifact was found; thus cant segment nor predict size: {path}")
            continue
        

        all_colors = get_dominant_color(original_image, artifact_contour)
        object_width = get_horizontal_dimension(artifact_contour, ppm, config) 

        if object_width != 0.0:
            if pearl_view == 'A':
                length_viewA.append(object_width)
            else:
                width_viewB.append(object_width) 
        else:
            print('The scale contour wasnt detected so the object couldnt be measured') # TODO: logging

        if pearl_view == 'A':
                all_dom_colors.append(np.array(all_colors))  

        if merge:
            output_file = pearl_id
            images.append(original_image)
            out_contours.append(artifact_contour) 
            in_contours.append(inner_contour)
        else:
            output_file = parse_filename_from_path(path)
            canvas = place_obj_on_background([original_image], [artifact_contour], [inner_contour], transparent, config)
            processed_images[output_file] = canvas

    if merge: 
        canvas = place_obj_on_background(images, out_contours, in_contours, transparent, config)
        processed_images[output_file] = canvas

    final_object_length = round(sum(length_viewA) / len(length_viewA), 1) if length_viewA else 0.0
    final_object_width = round(sum(width_viewB) / len(width_viewB), 1) if width_viewB else 0.0

    dom_color = all_dom_colors[0] if all_dom_colors else None


    return processed_images, final_object_length, final_object_width, dom_color

