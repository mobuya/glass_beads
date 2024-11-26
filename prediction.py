import cv2
from find_object import find_artifact_contour
from size_calculation import get_horizontal_dimension
from pixel_per_metric import calculate_ppm
from id_parser import parse_pearl_id_from_path, parse_pearl_id_and_view

'''
save always the previous pixel per metric so if the picture cant see the scale on the image take it from the previous one
'''

def process_object_size(paths, configuration):
    length_viewA = []
    width_viewB = []

    for path in paths:
        pealr_id, view = parse_pearl_id_and_view(parse_pearl_id_from_path(path))
        pearl_view = 'A' if "A" in view else 'B'
        print(f"For pearl {pealr_id} process view {view}")

        ppm = calculate_ppm(path, 50, configuration)
        object_contour, _ = find_artifact_contour(path, 'X', configuration)  # pearl view is X because its irelevant here
        
        object_width = get_horizontal_dimension(object_contour, ppm, configuration) 

        if object_width != 0.0:
            if pearl_view == 'A':
                length_viewA.append(object_width)
            else:
                width_viewB.append(object_width) 
        
        print(f"Done with view {view}")

    final_object_length = sum(length_viewA) / len(length_viewA) if length_viewA else 0.0
    final_object_width = sum(width_viewB) / len(width_viewB) if width_viewB else 0.0


    return round(final_object_length, 1), round(final_object_width, 1)
            



