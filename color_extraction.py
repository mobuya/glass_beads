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


def get_dominant_color(img, contour, nr_colors=3, nr_iter=10, eps=10):
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
