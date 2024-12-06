import cv2
import numpy as np

 
def get_horizontal_dimension(pearl_contour, pixel_metric, configuration):
    if pixel_metric is None:
        return 0.0        
    if pearl_contour is None:
        print('No valid contour found for size prediction.')
        return 0.0

   
    _, _, w, _ = cv2.boundingRect(pearl_contour)
    
    measured_width = w / pixel_metric  

    # Adjust for dilation adaptation
    DILATE_ADAPTATION = configuration["DILATE_ADAPTATION"]   # THIS DEPENDS ALSO ON THE IMAGE RESOLUTIN

    measured_width = measured_width - DILATE_ADAPTATION
    measured_width = round(measured_width, 1)

    return measured_width
