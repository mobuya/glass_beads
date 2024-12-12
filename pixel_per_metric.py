import cv2
import numpy as np
from enhance_threshold import enhance_and_threshold
from imutils import perspective
from scipy.spatial import distance as dist
from find_object import get_background_color
 

template_path = "fitted_color_palette.png"

def calculate_ppm(image_path, scale_length, configuration,  thr_value = 160):  # im not sure which value to use for the scale tbh
    original_image = cv2.imread(image_path)

    threshold_image = enhance_and_threshold(original_image, configuration, True,  thr_value)

    image_h,_ , _ = original_image.shape

    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    MIN_SCALE_AREA = configuration["MIN_SCALE_AREA"]

    scale_contour = None
    pixel_metric = None

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if hierarchy[0][idx][3] == -1 and area > MIN_SCALE_AREA:  #  just look at outer contours
           x, y, w, h = cv2.boundingRect(contour)
           if y > (image_h * 0.5):
               scale_contour = contour
               break
        

    '''
    In case the scale contour cant be found it is usually due to the scale and color palette being to close to each other.
    Removing the color palette(template) from the image makes it easier to find the scale contour.
    If this also results in no contour, either the scale is not present or the image has an invalid format for this tool.
    '''
    if scale_contour is None:
        print('Inside the new function that removes the color palette if the scale is not found.')
        bg_color = get_background_color(original_image)
        template = cv2.imread(template_path,cv2.IMREAD_GRAYSCALE)
        best_method = 'TM_CCOEFF_NORMED'  # robust against light and some other invariance 

        img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        method = getattr(cv2, best_method)
        res = cv2.matchTemplate(img,template,method)
        _, _, _, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(original_image, top_left, bottom_right, bg_color, -1)

        threshold_image = enhance_and_threshold(original_image, configuration, True,  160)
        contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if hierarchy[0][idx][3] == -1 and area > MIN_SCALE_AREA:  #  just look at outer contours
                x, y, w, h = cv2.boundingRect(contour)
                if y > (image_h * 0.5):
                    print('It found a valid scale contour')
                    scale_contour = contour
                    break

    
    if scale_contour is not None:
        box = cv2.minAreaRect(scale_contour)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        
        (tl, tr, br, bl) = box
        
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        
        # measure the euclidian distance between the midpoints
        scale_width = dist.euclidean((tlblX, tlblY), (trbrX,trbrY))

        known_scale_length = scale_length # its in mm

        pixel_metric = scale_width / known_scale_length  # the width in the image should be irl 5 cm/ 50 mm
    else:
        print('There is no scale on this image bruv.')

       
    return pixel_metric # can return none, careful

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)