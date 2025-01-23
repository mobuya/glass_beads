import cv2
import logging

import numpy as np
from processing.pixel_per_metric import midpoint
from imutils import perspective
from scipy.spatial import distance as dist

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level


 
def get_horizontal_dimension(pearl_contour, pixel_metric, configuration):
    '''
    Calculates the horizontal (width) dimension of a bead in millimeters.

    Parameters
    ----------
    pearl_contour : numpy.ndarray
        The contour of the detected bead.

    pixel_metric : float
        Pixels per millimeter ratio derived from the scale in the image.

    configuration : dict
        Configuration dictionary containing "DILATE_ADAPTATION"- correction value for dilation effects in pixels.

    Returns
    -------
    measured_width: float
        The width of the pearl in millimeters, adjusted for dilation, rounded to one decimal place.
        Returns 0.0 if the scale or pearl contour is missing.
    '''
    # cannot reach these conditions because these values are checked before the function is called: but just to be safe
    if pixel_metric is None:
        logger.warning(f"No valid scale contour to be used for size calculation.")
        return 0.0        
    if pearl_contour is None:
        logger.warning(f"No valid object contour to be used for size calculation.")
        return 0.0  

    box = cv2.minAreaRect(pearl_contour)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    
    (tl, tr, br, bl) = box
    
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
        
    measured_width = dist.euclidean((tlblX, tlblY), (trbrX,trbrY)) 

    measured_width = measured_width / pixel_metric

    DILATE_ADAPTATION = configuration["DILATE_ADAPTATION"] 

    measured_width = measured_width - DILATE_ADAPTATION
    measured_width = round(measured_width, 1)

    return measured_width
