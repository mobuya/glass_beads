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
    all_dom_colors = []

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
        
            if artifact_contour is None:
                img_paths.remove(path)
                '''
                ********************* Here i need some logging like this image was not valid for merging thus it was skipped
                '''
                print('For image no artifact was found; thus cant segment nor predict size')
                continue

            out_contours.append(artifact_contour) 
            in_contours.append(inner_contour)
            object_width = get_horizontal_dimension(artifact_contour, ppm, config) 

            if object_width != 0.0:
                if pearl_view == 'A':
                    length_viewA.append(object_width)
                    all_dom_colors.append(np.array(all_colors))
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
            print(f"For pearl {pearl_view}")

            if artifact_contour is None:
                # ************* Here also logging like this contour was not found thus it was skipped
                print('For image no artifact was found; thus cant segment nor predict size')
                continue
        
            object_width = get_horizontal_dimension(artifact_contour, ppm, config) 

            if object_width != 0.0:
                if pearl_view == 'A':
                    length_viewA.append(object_width)
                    all_dom_colors.append(np.array(all_colors))
                else:
                    width_viewB.append(object_width) 
            else:
                print('No object found')

            canvas = place_obj_on_background([path], [artifact_contour], [inner_contour], transparent, config)
            processed_images[outfile] = canvas

    '''
    maybe look into what if it cant ever find the size/scale what to do
    '''
    final_object_length = round(sum(length_viewA) / len(length_viewA), 1) if length_viewA else 0.0
    final_object_width = round(sum(width_viewB) / len(width_viewB), 1) if width_viewB else 0.0

    dom_color = all_dom_colors[0] if all_dom_colors else None


    return processed_images, final_object_length, final_object_width, dom_color

