import numpy as np
import cv2
from id_parser import parse_filename_from_path, parse_pearl_id_and_view
from place_object import place_obj_on_background
from find_object import find_artifact_contour_and_color
from size_calculation import get_horizontal_dimension
from pixel_per_metric import calculate_ppm



def crop_artifact_and_measure(paths, config, merge, transparent, scale_size):
    processed_images = {}
    length_viewA = []
    width_viewB = []
    all_dom_colors = []

    out_contours = []
    in_contours = []
    images = []

    for path in paths:
        pearl_id, pearl_view =  parse_pearl_id_and_view(parse_filename_from_path(path))
        pearl_view = 'A' if "A" in pearl_view else 'B'
        
        original_image = cv2.imread(path)

        ppm = calculate_ppm(original_image, scale_size, config)

        artifact_contour, inner_contour, all_colors = find_artifact_contour_and_color(original_image, pearl_view, config) # maybe i can split later then the color from img
    
        if artifact_contour is None:
            '''
            ********************* Here also logging like this contour was not found thus it was skipped, save to a log or smth
            '''
            print(f"For image no artifact was found; thus cant segment nor predict size: {path}")
            continue

        object_width = get_horizontal_dimension(artifact_contour, ppm, config) 

        if object_width != 0.0:
            if pearl_view == 'A':
                length_viewA.append(object_width)
                all_dom_colors.append(np.array(all_colors))  # colors are only extracted from view a, b is skipped cus of the hole
            else:
                width_viewB.append(object_width) 
        else:
            print('No object found')

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

