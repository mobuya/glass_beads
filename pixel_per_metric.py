import cv2
import numpy as np
from enhance_threshold import enhance_and_threshold
from imutils import perspective
from scipy.spatial import distance as dist
from id_parser import parse_filename_from_path
 

def calculate_ppm(image_path, scale_length, configuration,  thr_value = 160):  # im not sure which value to use for the scale tbh
    original_image = cv2.imread(image_path)
    # print('in calculate ppm the image_path is:', image_path)

    threshold_image = enhance_and_threshold(original_image, configuration, True,  thr_value)

    image_h,_ , _ = original_image.shape

    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    MIN_SCALE_AREA = configuration["MIN_SCALE_AREA"]
    scale_contour = None

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if hierarchy[0][idx][3] == -1 and area > MIN_SCALE_AREA:  #  just look at outer contours
           x, y, w, h = cv2.boundingRect(contour)
           if y > (image_h * 0.5):
               scale_contour = contour
               break
        
    pixel_metric = None

    
    if scale_contour is not None:
        box = cv2.minAreaRect(scale_contour)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        cv2.drawContours(original_image, [box.astype("int")], -1, (0,255,0), 2)

        (tl, tr, br, bl) = box
        
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        
        # measure the euclidian distance between the midpoints
        scale_width = dist.euclidean((tlblX, tlblY), (trbrX,trbrY))

        known_scale_length = scale_length # its in mm

        pixel_metric = scale_width / known_scale_length  # the width in the image should be irl 5 cm/ 50 mm
        #cv2.imwrite('found_bigger_dilate.jpg', threshold_image)
    else:
        pearl_name = parse_filename_from_path(image_path)
        cv2.imwrite(f"invalid_scale_{pearl_name}.jpg", threshold_image)
        print('Scale contour was not found: too close to board or in an invalid position.')

    return pixel_metric # can return none, careful

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)