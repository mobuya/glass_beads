import numpy as np

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
