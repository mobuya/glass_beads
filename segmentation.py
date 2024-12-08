import cv2
import numpy as np
from id_parser import parse_filename_from_path
from id_parser import parse_pearl_id_and_view
from find_object import find_artifact_contour
from place_object import place_obj_on_background



def process_images(paths, config, merge, transparent):
    processed_images = {}

    if merge:
        out_contours = []
        in_contours = []
        img_paths = []
        for path in paths:
            img_paths.append(path)
            pearl_id, _ =  parse_pearl_id_and_view(parse_filename_from_path(path))
            
            print('path is', path)
            _, pearl_view = parse_pearl_id_and_view(path)
            pearl_view = 'A' if "A" in pearl_view else 'B'
            
            artifact_contour, inner_contour = find_artifact_contour(path, pearl_view, config)

            out_contours.append(artifact_contour) 
            in_contours.append(inner_contour)

        canvas = place_obj_on_background(img_paths, out_contours, in_contours, transparent, config)
        print(f"----> the merge output file {pearl_id}")
        processed_images[pearl_id] = canvas
    else:
        for path in paths:
            outputfile = parse_filename_from_path(path)
            
            print('path is', path)
            _, pearl_view = parse_pearl_id_and_view(path)
            pearl_view = 'A' if "A" in pearl_view else 'B'
            
            artifact_contour, inner_contour = find_artifact_contour(path, pearl_view, config)

            canvas = place_obj_on_background([path], [artifact_contour], [inner_contour], transparent, config)
            processed_images[outputfile] = canvas

    return processed_images
