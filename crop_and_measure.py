import numpy as np
from id_parser import parse_filename_from_path, parse_pearl_id_and_view
from place_object import place_obj_on_background
from find_object import find_artifact_contour_and_color
from size_calculation import get_horizontal_dimension
from pixel_per_metric import calculate_ppm

'''
each path is per pearl ID
'''

ORIGINAL_SCALE_SIZE_mm = 50

def crop_artifact_and_measure(paths, config, merge, transparent):
    processed_images = {}
    length_viewA = []
    width_viewB = []
    dom_colors = []

    if merge:
        out_contours = []
        in_contours = []
        img_paths = []
        for path in paths:
            img_paths.append(path)
            pearl_id, pearl_view =  parse_pearl_id_and_view(parse_filename_from_path(path))
            
            pearl_view = 'A' if "A" in pearl_view else 'B'
            ppm = calculate_ppm(path, ORIGINAL_SCALE_SIZE_mm, config)

            artifact_contour, inner_contour, all_colors = find_artifact_contour_and_color(path, pearl_view, config) # maybe i can split later then the color from img
        
            out_contours.append(artifact_contour) 
            in_contours.append(inner_contour)
            object_width = get_horizontal_dimension(artifact_contour, ppm, config) 

            if object_width != 0.0:
                if pearl_view == 'A':
                    length_viewA.append(object_width)
                    dom_colors.append(np.array(all_colors))
                else:
                    width_viewB.append(object_width) 
            else:
                print('No object found')

        canvas = place_obj_on_background(img_paths, out_contours, in_contours, transparent, config)
        processed_images[pearl_id] = canvas
    else:
        for path in paths:
            outfile = parse_filename_from_path(path)
            
            pearl_id, pearl_view =  parse_pearl_id_and_view(parse_filename_from_path(path))
            
            pearl_view = 'A' if "A" in pearl_view else 'B'
            ppm = calculate_ppm(path, ORIGINAL_SCALE_SIZE_mm, config)

            artifact_contour, inner_contour, all_colors = find_artifact_contour_and_color(path, pearl_view, config)
        
            object_width = get_horizontal_dimension(artifact_contour, ppm, config) 

            if object_width != 0.0:
                if pearl_view == 'A':
                    length_viewA.append(object_width)
                    dom_colors.append(np.array(all_colors))
                else:
                    width_viewB.append(object_width) 
            else:
                print('No object found')

            canvas = place_obj_on_background([path], [artifact_contour], [inner_contour], transparent, config)
            processed_images[outfile] = canvas

    final_object_length = sum(length_viewA) / len(length_viewA) if length_viewA else 0.0
    final_object_width = sum(width_viewB) / len(width_viewB) if width_viewB else 0.0

    return processed_images, final_object_length, final_object_width, dom_colors[0]
