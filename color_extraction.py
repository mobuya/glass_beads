import cv2
import numpy as np
from matplotlib import pyplot as plt


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


def get_dominant_color(img, contour, nr_colors=3, nr_iter=10, eps=10):
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
    - If no contour is provided, the function prints a warning and returns `None`. !!!!!!!!!!!!!!!!!!!!!!!! 
    '''  

    if contour is None:
        print('No contour found: contour function could not be called.')
        return None  # TODO: Error handling here 

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

    masked_img = cv2.bitwise_and(img, img, mask=mask)

    roi = masked_img[mask == 255]

    reshaped_img = roi.reshape(-1, 3).astype(np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, nr_iter, eps)

    _, _, col_centers = cv2.kmeans(reshaped_img, nr_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    col_centers = np.uint8(col_centers)

    col_centers = np.sort(col_centers, axis=0)

    return col_centers
