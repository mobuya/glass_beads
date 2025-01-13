import cv2
import numpy as np


def enhance_and_threshold(image, configuration, threshold_value = 223, CLAHE_BOOL = False):
    # original ist 7952x5304
    MORPH_KERNEL_SIZE = configuration["MORPH_KERNEL_SIZE"]
    MORPH_ITERATIONS = configuration["MORPH_ITERATIONS"]
    DILATE_KERNEL_SIZE = configuration["DILATE_KERNEL_SIZE"]
    DILATE_ITERATIONS = configuration["DILATE_ITERATIONS"]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    img = cv2.medianBlur(gray, 5)

    if CLAHE_BOOL:
        clahe = cv2.createCLAHE(clipLimit=0.9, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(img)
        _, threshold_image = cv2.threshold(enhanced_image, threshold_value, 255, cv2.THRESH_BINARY_INV)
    else:   
        _, threshold_image = cv2.threshold(img, threshold_value,255,cv2.THRESH_BINARY_INV)  

    img = cv2.medianBlur(threshold_image, 15)  

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, MORPH_KERNEL_SIZE, iterations=MORPH_ITERATIONS) 
    
    smooth_outline = cv2.dilate(closing, DILATE_KERNEL_SIZE, iterations=DILATE_ITERATIONS)
    
    return smooth_outline
