import cv2
import numpy as np
from imutils import perspective
from scipy.spatial import distance as dist

from processing import enhance_and_threshold, get_background_color

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level


template_path = "processing/size_and_color/fitted_color_palette.png"

def calculate_ppm(original_image, scale_length, configuration,  thr_value = 180):
    '''
    Calculates the pixel-per-millimeter (ppm) ratio based on the detected scale in the image.

    This function identifies the scale bar in the image and computes how many pixels correspond to one millimeter using the known physical length of the scale.

    Parameters
    ----------
    original_image : numpy.ndarray
        The input image containing the scale bar.

    scale_length : float
        The real-world length of the scale bar in millimeters (e.g., 50 for a 5 cm scale).

    configuration : dict
        Configuration dictionary with processing parameters, including:
            - "MIN_SCALE_AREA": Minimum area to consider a contour as the scale.

    thr_value : int, optional (default=180)
        Threshold value for binary thresholding; pixels below this value are set to 255 (white), and above to 0 (black).

    Returns
    -------
    pixel_metric : float or None
        The calculated pixel-per-millimeter ratio; returns None if the scale cannot be detected.

    Notes
    -----
    - If the scale bar is not detected, the function attempts to remove the color palette using template matching and retries the detection.
    - IMPORTANT: The function assumes the scale is located in the lower half of the image!
    '''
  
    threshold_image = enhance_and_threshold(original_image, configuration, thr_value)  # CHANGES HERE TO FALSE

    image_h,_ , _ = original_image.shape

    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    MIN_SCALE_AREA = configuration["MIN_SCALE_AREA"]

    scale_contour = None
    pixel_metric = None

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if hierarchy[0][idx][3] == -1 and area > MIN_SCALE_AREA: 
           x, y, w, h = cv2.boundingRect(contour)
           if y > (image_h * 0.5):
               scale_contour = contour
               break
        

    '''
    In case the scale contour cant be found it is usually due to the scale and color palette being too close to each other.
    Removing the color palette (template) from the image makes it easier to find the scale contour.
    If this also results in no contour, either the scale is not present or the image has an invalid format for this tool.
    '''
    if scale_contour is None:
        logger.info(f"Inside the template matching function since the original function could not find a valid scale contour.")
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

        threshold_image = enhance_and_threshold(original_image, configuration, 160)
        contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if hierarchy[0][idx][3] == -1 and area > MIN_SCALE_AREA: 
                x, y, w, h = cv2.boundingRect(contour)
                if y > (image_h * 0.5):
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
        
        scale_width = dist.euclidean((tlblX, tlblY), (trbrX,trbrY))

        known_scale_length = scale_length 

        pixel_metric = scale_width / known_scale_length
    else:
        logger.warning("Failed to find the scale outline on image!")

       
    return pixel_metric

def midpoint(ptA, ptB):
    '''
    Calculates the midpoint between two points.
    Euclidean distance

    Parameters
    ----------
    ptA : tuple
        The (x, y) coordinates of the first point.
    ptB : tuple
        The (x, y) coordinates of the second point.

    Returns
    -------
    midpoint: tuple
        The (x, y) coordinates of the midpoint between ptA and ptB.
    '''

    midpoint = ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
    return midpoint