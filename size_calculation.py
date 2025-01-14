import cv2

 
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
    if pixel_metric is None:
        print('The scale contour could not be calculated.')
        return 0.0        
    if pearl_contour is None:
        print('No valid contour found for size prediction.')
        return 0.0 # TODO: Logging, error handling 

    _, _, w, _ = cv2.boundingRect(pearl_contour)
    
    measured_width = w / pixel_metric  

    
    DILATE_ADAPTATION = configuration["DILATE_ADAPTATION"]   # TODO: THIS DEPENDS ALSO ON THE IMAGE RESOLUTION

    measured_width = measured_width - DILATE_ADAPTATION
    measured_width = round(measured_width, 1)

    return measured_width
