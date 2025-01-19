import cv2
import numpy as np
from enhance_threshold import enhance_and_threshold
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level


THR_VALUE = 223  
BACKGROUND_SIMILARITY_TOLERANCE = 25
HOLE_SIMILARITY_TOLERANCE = 10  

def find_artifact_contour(original_image, bead_view, configuration, thr_value = THR_VALUE, hole_similarity = HOLE_SIMILARITY_TOLERANCE, clahe = False):
    '''
    Detects the contour of the artifact (bead) in the image, returning also the hole contour for proper bead view. 
    In case of a bead having a similar color to the background, a new threshold function is called.

    Parameters
    ----------
    original_image : numpy.ndarray
        The input image of the bead, where the contour is found.

    bead_view : str
        Indicates the view of the bead ('A' for front view, 'B' for hole view).

    configuration : dict 
        Dictionary containing processing parameters.

    thr_value : int, optional (default=223)
        Threshold value used for image binarization. Defaults to a predefined constant `THR_VALUE`.

    hole_similarity : int, optional (default=10)
        Tolerance for determining similarity between the inner contour color and background color. 

    clahe : bool, optional (default=False)
        Flag to enable Contrast Limited Adaptive Histogram Equalization (CLAHE) for better contrast. 
        Used when beads color too similar too background, otherwise its contours aren't clean.

    Returns
    -------
    smallest_contr : numpy.ndarray or None
        The detected outer contour of the artifact; returns `None` if not found.

    inner_contour : numpy.ndarray or None
        The detected inner contour (for pearls with holes, i.e., view B); returns `None` if not found.

    Notes
    -----
    - If no contour was found, the function is called again with a new threshold value of 160. 
      Also changing the hole similarity to 25, since mainly the function is called again if the brightness is too low.
    - IMPORTANT: The function assumes the bead is around the middle of the image, and returns the first found contour that fulfills the following criteria:
        * it's an outer contour
        * the area is bigger than configuration["MIN_AREA"] and smaller than 1/3 of the image
        * it upper left corner is within the upper 80% of the image height and the left 50% of the image width

    !!!
    PLEASE follow a consistent image layout for this function to return optimal solutions!
    !!!
    '''

    threshold_image = enhance_and_threshold(original_image, configuration, thr_value, clahe)
    background_color = get_background_color(original_image)

    image_h, image_w, _ = original_image.shape

    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
   
    smallest_contr = None
    inner_contour = None

    #temp_img = original_image.copy()
    MIN_AREA = configuration["MIN_AREA"] 
    INNER_AREA_LIMIT = configuration["INNER_AREA"]

    area_limit = (image_h * image_w) / 3  # look into this maybe

    for idx, contour in enumerate(contours):
        #area = cv2.contourArea(contour)
        rect = cv2.boundingRect(contour)
        x,y,w,h = rect
        area = w * h
        if hierarchy[0][idx][3] == -1:  
            if area >= MIN_AREA:
                x, y, _, _ = cv2.boundingRect(contour)
                if y < (image_h * 0.8) and x < (image_w * 0.5) and area < area_limit:  

                    mask = np.zeros(threshold_image.shape, dtype=np.uint8)
                    cv2.drawContours(mask, [contour], -1, 255, -1)
                    mean_color = cv2.mean(original_image, mask=mask)[:3]  
                    
                    if np.allclose(mean_color, background_color, atol=BACKGROUND_SIMILARITY_TOLERANCE):
                        logger.info("A contour was detected but it's color was too similar to the background; thus it was skipped")
                        continue  

                    if not clahe:
                        if np.allclose(mean_color, background_color, atol=60): 
                            logger.info(f"A contour was detected which color is similar too background; called new thresholding function to get cleaner outline.")
                            logger.info(f"IMPORTANT: check the output for this bead, since there might be a chance the output is not clean (!!!)")
                            return find_artifact_contour(original_image, bead_view, configuration, thr_value, hole_similarity, clahe=True)  
                                           
                    smallest_contr = contour
                    
                    for sub_index, sub_contour in enumerate(contours):
                        if hierarchy[0][sub_index][3] == idx and bead_view == 'B':
                            inner_area = cv2.contourArea(sub_contour)
                            if inner_area > INNER_AREA_LIMIT:  
                                
                                inner_mask = np.zeros(threshold_image.shape, dtype=np.uint8)
                                cv2.drawContours(inner_mask, [sub_contour], -1, 255, -1)
                                inner_mean_color = cv2.mean(original_image, mask = inner_mask)[:3]

                                if np.allclose(inner_mean_color, background_color, atol = hole_similarity):  
                                    inner_contour = sub_contour
                                    break
            
                    break


    if smallest_contr is None:
        if thr_value != 160:
            new_thr_value = 160
            NEW_HOLE_SIMILARITY_TOLERANCE = 25 
            logger.info(f"No bead outline found: calling the function once again with a threshold value of 160.")
            return find_artifact_contour(original_image, bead_view,configuration, new_thr_value, NEW_HOLE_SIMILARITY_TOLERANCE) 

            
    return smallest_contr, inner_contour
    

def get_background_color(image):
    '''
    Estimates the background color of an image by averaging the colors of its four corners.
    This function works for this tool since the image layout is consistent, thus having clear corners.
    
    Parameters
    ----------
    image : numpy.ndarray
        The input image whose background color is to be determined.

    Returns
    -------
    background_color : numpy.ndarray
        The estimated background color as a 3-element array representing the (BGR) color values.
    '''
    corners = [image[0, 0], image[0, -1], image[-1, 0], image[-1, -1]]
    corner_samples = np.array(corners)
    
    background_color = corner_samples.mean(axis=0)

    return background_color
