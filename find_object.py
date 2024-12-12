import cv2
import numpy as np
from enhance_threshold import enhance_and_threshold
from color_extraction import get_dominant_color


THR_VALUE = 223
BACKGROUND_SIMILARITY_TOLERANCE = 25
HOLE_SIMILARITY_TOLERANCE = 10  

def find_artifact_contour_and_color(image_path, pearl_view, configuration, thr_value = THR_VALUE, hole_similarity = HOLE_SIMILARITY_TOLERANCE):
    original_image = cv2.imread(image_path)
    threshold_image = enhance_and_threshold(original_image, configuration, False, thr_value)
    dominant_color = None

    background_color = get_background_color(original_image)

    image_h, image_w, _ = original_image.shape

    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
   
    smallest_contr = None
    inner_contour = None

    MIN_AREA = configuration["MIN_AREA"] 
    INNER_AREA_LIMIT = configuration["INNER_AREA"]

    area_limit = (image_h * image_w) / 3  # look into this maybe

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if hierarchy[0][idx][3] == -1:  #  just look at outer contours
            if area >= MIN_AREA:
                x, y, _, _ = cv2.boundingRect(contour)
                if y < (image_h * 0.8) and x < (image_w * 0.5) and area < area_limit:  # check position and area size

                    mask = np.zeros(threshold_image.shape, dtype=np.uint8)
                    cv2.drawContours(mask, [contour], -1, 255, -1)
                    mean_color = cv2.mean(original_image, mask=mask)[:3]  # get color of the found area; cant be too similar
                    
                    if np.allclose(mean_color, background_color, atol=BACKGROUND_SIMILARITY_TOLERANCE):
                        continue  
                    
                    smallest_contr = contour

                    for sub_index, sub_contour in enumerate(contours):
                        if hierarchy[0][sub_index][3] == idx and pearl_view == 'B':
                            inner_area = cv2.contourArea(sub_contour)
                            if inner_area > INNER_AREA_LIMIT:  
                                
                                inner_mask = np.zeros(threshold_image.shape, dtype=np.uint8)
                                cv2.drawContours(inner_mask, [sub_contour], -1, 255, -1)
                                inner_mean_color = cv2.mean(original_image, mask = inner_mask)[:3]

                                if np.allclose(inner_mean_color, background_color, atol = hole_similarity):  # similarity tol changed for 340_139 -> 10 works, for rethresh
                                    inner_contour = sub_contour
                                    break

                    break


    if smallest_contr is not None:
        print('Artifact contour found.')
    else:
        if thr_value != 160:
            THR_VALUE = 160
            NEW_HOLE_SIMILARITY_TOLERANCE = 25
            return find_artifact_contour_and_color(image_path, pearl_view,configuration, 160, NEW_HOLE_SIMILARITY_TOLERANCE) # add logging for the change of the value

         # ERROR HANDLING HERE: means image is not adaptable for threshold
    
    # ****************** COLOR EXTRACTION ******************
    '''
    Color extraction is places here because of optimization issues !!!
    '''
    if smallest_contr is not None:
        dominant_color = get_dominant_color(original_image, smallest_contr)
        
    return smallest_contr, inner_contour, dominant_color
    

def get_background_color(image):
    '''
    Find background color by extracting the colors of the 4 corners and taking the mean.

    Parameters:
    ----------

    image: image to calculate the background of.
    '''
    corners = [image[0, 0], image[0, -1], image[-1, 0],   image[-1, -1]]
    corner_samples = np.array(corners)
    
    background_color = corner_samples.mean(axis=0)

    return background_color