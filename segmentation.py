import cv2
import numpy as np
from id_parser import parse_pearl_id_from_path
from id_parser import parse_pearl_id_and_view
from enhance_threshold import enhance_and_threshold
from find_object import find_artifact_contour
from place_object import place_object_on_background


'''

Merge tells us if we merge two views or not


I need info somewhere if its png or white background

!!!!!!!!!
Transparent toggle is here !!!!!!!! ITS AT TRUE THE TRANSPARENT

'''

def process_images(paths, merge = False):
    processed_images = {}
    transparent = True

    if merge:
        print('merging')
        # loop over images and save contours in a list
        # call a separate function for merging multiple objects
        # that function has to deal with the placement of multiple objects at once
        # could also maybe be done with the down same function 
    else:
        for path in paths:
            outputfile = parse_pearl_id_from_path(path)
            
            print('path is', path)
            _, pearl_view = parse_pearl_id_and_view(path)
            pearl_view = 'A' if "A" in pearl_view else 'B'
            
            artifact_contour, inner_contour = find_artifact_contour(path, pearl_view, config)
            final_img = place_object_on_background(path, artifact_contour, inner_contour, transparent=transparent)
            
            processed_images[outputfile] = final_img
            #print('output:', outputfile)

    return processed_images


'''
for now split functions of segmentation and size prediction

'''


def process_scale(paths):
    output_list = []
    for path in paths:
        image = cv2.imread(path)
        thr_img = enhance_and_threshold(image, 200)

        contours, _ = cv2.findContours(thr_img,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000000 and area < 9000000:  # for original image size
                print('area:', area)
                #cv2.drawContours(image, [cnt], 0, (0,0,0), 5)
                x, y, w, h = cv2.boundingRect(cnt)  
                if x < 100:  # the position of the top left corner has to be under a specific part
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
                    print('top left coordinate: ', x, y, 'width, heigth: ', w, h)
                        
        output_list.append(image)

    return output_list