from contextlib import contextmanager
import constants
import cv2

@contextmanager
def config_context(path):
    '''
    Provides a configuration object based on the size of the input image.  
    This configuration adapts parameters for image processing tasks such as dilation and morphing, which are sensitive to pixel dimensions.

    Parameters
    ----------
    path : str
        The file path to the input image.

    Yields
    ------
    config : dict
        A configuration dictionary selected from `constants.PREDEFINED_CONFIGS` based on the image size.
        - `"max_size"` is used for very large images (> 35,000,000 pixels).  
        - `"min_size"` is used for moderately large images (> 20,000,000 pixels).  

    Raises
    ------
    ValueError
        If the image size is smaller than or equal to 20,000,000 pixels or if the image cannot be read.

    Notes
    -----
    To use this context manager, apply it as follows:

      ```python
      with config_context("image_path.png") as config:
          # use config object for processing
      ```
    '''

    img = cv2.imread(path)
    image_pixels = img.shape[0] * img.shape[1]

    if image_pixels > 35000000:
        config = constants.PREDEFINED_CONFIGS["max_size"]
    elif image_pixels > 20000000:
        config = constants.PREDEFINED_CONFIGS["min_size"]
    else:
        raise ValueError("Invalid image size!") # TODO: Error handling 

    yield config
