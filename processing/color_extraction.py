import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level


'''
****************************************
Author: Andrii Skabrii
Date: 01.12.2024 
File: colors-glassbeads-clustering.ipynb
****************************************
'''

'''

Work with param values to maybe get better results 

'''


def get_dominant_colors(images, contours, inner_contours, nr_colors=3, nr_iter=100, eps=300):
    '''
    Extracts the dominant colors within a specified contour region of an image using K-Means clustering.

    Parameters
    ----------
    img : numpy.ndarray
        The input image.

    contour : numpy.ndarray
        The contour defining the region of interest (ROI) from which to extract dominant colors.

    nr_colors : int, optional (default=3)
        The number of dominant colors to extract.

    nr_iter : int, optional (default=10)
        The maximum number of iterations for the K-Means clustering algorithm.

    eps : float, optional (default=10)
        The epsilon value for the K-Means convergence criteria.

    Returns
    -------
    col_centers : numpy.ndarray
        An array of RGB color values representing the dominant colors within the specified contour.
        The array shape is (nr_colors, 3), where each row corresponds to a dominant color.

    Notes
    -----
    - If no contour is provided, the function logs an info and returns `None`. 
    '''  

    object_sizes = [(cv2.boundingRect(c)[2], cv2.boundingRect(c)[3]) for c in contours]
    object_heights = [cv2.boundingRect(c)[3] for c in contours]
    object_widths = [cv2.boundingRect(c)[2] for c in contours]
  
    canvas_width = sum(object_widths) + (len(object_widths) - 1) 
    canvas_height = max(object_heights)
    canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)  

    
    current_x = 0

    for img, contour, inner_contour, (w, h) in zip(images, contours, inner_contours, object_sizes):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        if inner_contour is not None:
            cv2.drawContours(mask, [inner_contour], -1, 0, thickness=cv2.FILLED)
        extracted_artifact = cv2.bitwise_and(img, img, mask=mask)
         
        x, y, w, h = cv2.boundingRect(contour)
        roi = extracted_artifact[y:y+h, x:x+w]
        cropped_mask = mask[y:y+h, x:x+w]


        artifact = np.zeros((h, w, 4), dtype=np.uint8)
        artifact[..., :3] = roi
        artifact[..., 3] = cropped_mask

        
        h_offset = (canvas_height - h) // 2 
        canvas[h_offset:h_offset + h, current_x:current_x + w] = artifact

        current_x += w


    
    rgb_canvas = canvas[..., :3]
    alpha_channel = canvas[..., 3]

    valid_pixels = rgb_canvas[alpha_channel > 0]

    reshaped_img = valid_pixels.reshape(-1, 3).astype(np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, nr_iter, eps)  # (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, nr_iter, eps)

    _, _, col_centers = cv2.kmeans(reshaped_img, nr_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    col_centers = np.uint8(col_centers)

    col_centers = np.sort(col_centers, axis=0)

    
    return col_centers




def get_all_dominant_color(images, contours, inner_contours, nr_colors=3, nr_iter=100, eps=300):

    object_sizes = [(cv2.boundingRect(c)[2], cv2.boundingRect(c)[3]) for c in contours]
    object_heights = [cv2.boundingRect(c)[3] for c in contours]
    object_widths = [cv2.boundingRect(c)[2] for c in contours]
  
    canvas_width = sum(object_widths) + (len(object_widths) - 1) 
    canvas_height = max(object_heights)
    canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)  

    
    current_x = 0

    for img, contour, inner_contour, (w, h) in zip(images, contours, inner_contours, object_sizes):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        if inner_contour is not None:
            cv2.drawContours(mask, [inner_contour], -1, 0, thickness=cv2.FILLED)
        extracted_artifact = cv2.bitwise_and(img, img, mask=mask)
         
        x, y, w, h = cv2.boundingRect(contour)
        roi = extracted_artifact[y:y+h, x:x+w]
        cropped_mask = mask[y:y+h, x:x+w]


        artifact = np.zeros((h, w, 4), dtype=np.uint8)
        artifact[..., :3] = roi
        artifact[..., 3] = cropped_mask

        
        h_offset = (canvas_height - h) // 2 
        canvas[h_offset:h_offset + h, current_x:current_x + w] = artifact

        current_x += w


    
    rgb_canvas = canvas[..., :3]
    alpha_channel = canvas[..., 3]

    valid_pixels = rgb_canvas[alpha_channel > 0]

    reshaped_img = valid_pixels.reshape(-1, 3).astype(np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, nr_iter, eps)  # (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, nr_iter, eps)

    _, _, col_centers = cv2.kmeans(reshaped_img, nr_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    col_centers = np.uint8(col_centers)

    col_centers = np.sort(col_centers, axis=0)

    
    return col_centers