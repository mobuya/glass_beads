import cv2
import numpy as np
from find_object import find_artifact_contour_and_color
from size_calculation import get_horizontal_dimension
from pixel_per_metric import calculate_ppm
from id_parser import parse_filename_from_path, parse_pearl_id_and_view


'''
save always the previous pixel per metric so if the picture cant see the scale on the image take it from the previous one:
but what to do if the first few pictures dont have a valid scale? 


in the main function, create values for min, max and average dimensions

'''

def process_object_size_color(paths, configuration):
    length_viewA = []
    width_viewB = []
    colors = []

    for path in paths:
        _, view = parse_pearl_id_and_view(parse_filename_from_path(path))
        pearl_view = 'A' if "A" in view else 'B'

        ppm = calculate_ppm(path, 50, configuration)
        object_contour, _, main_color = find_artifact_contour_and_color(path, 'X', configuration)  # pearl view is X because its irelevant here
        
        colors.append(main_color)

        object_width = get_horizontal_dimension(object_contour, ppm, configuration) 

        if object_width != 0.0:
            if pearl_view == 'A':
                length_viewA.append(object_width)
            else:
                width_viewB.append(object_width) 
        else:
            print('No object found')
        #print(f"Done with view {view}")


    final_object_length = sum(length_viewA) / len(length_viewA) if length_viewA else 0.0
    final_object_width = sum(width_viewB) / len(width_viewB) if width_viewB else 0.0

    # return just the first color for now, its sorted so its from view A (no hole): could add in find obj that it saves the color only if its view A 

    return round(final_object_length, 1), round(final_object_width, 1), colors[0]
            
