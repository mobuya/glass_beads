import cv2
import numpy as np
from enhance_threshold import enhance_and_threshold
from find_object import THR_VALUE

'''
Background transparent per default, if changed it is white 

For now per one object, should also be a posibility to loop through a list and combine many at once

'''


def place_object_on_background(image_path, outer_contour, inner_contour, transparent = True):   
    original_image = cv2.imread(image_path)
    img_h, img_w, _ = original_image.shape

    thr_img = enhance_and_threshold(original_image, THR_VALUE)  

    mask = np.zeros_like(thr_img)
    cv2.drawContours(mask, [outer_contour], -1, 255, thickness=cv2.FILLED)  # look if thickness correct

    if inner_contour is not None:
        cv2.drawContours(mask, [inner_contour], -1, 0, thickness=cv2.FILLED) 

    extracted_artifact = cv2.bitwise_and(original_image, original_image, mask=mask)

    if transparent is True:
        pearl_on_background = np.zeros((img_h, img_w, 4), dtype=np.uint8)
        pearl_on_background[..., :3] = extracted_artifact
        pearl_on_background[..., 3] = mask
    else:
         pearl_on_background = np.ones_like(original_image) * 255
         x, y, w, h = cv2.boundingRect(outer_contour)
         
         roi = pearl_on_background[y:y+h, x:x+w]
         mask_cropped = mask[y:y+h, x:x+w]
         object_cropped = extracted_artifact[y:y+h, x:x+w]
         
         roi[mask_cropped > 0] = object_cropped[mask_cropped > 0]

    return pearl_on_background
