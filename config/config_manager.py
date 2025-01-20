from contextlib import contextmanager
import config.constants as constants
import cv2
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level

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
    - yields None if it raises errors

    To use this context manager, apply it as follows:

      ```python
      with config_context("image_path.png") as config:
          # use config object for processing
      ```
    '''
    try:
        img = cv2.imread(path)

        if img is None:
            raise FileNotFoundError(f"The following path could not open an image: {path}")
   
        # RESIZING PART 2!
        #img = cv2.resize( img, (6000, 4000))
        #img = cv2.resize( img, (6600, 4400))
        #img = cv2.resize( img, (7000, 4667))
        #img = cv2.resize( img, (7500, 5000))

        image_pixels = img.shape[0] * img.shape[1]

        if image_pixels > 35000000:
            config = constants.PREDEFINED_CONFIGS["max_size"]
        elif image_pixels > 20000000:
            config = constants.PREDEFINED_CONFIGS["min_size"]
        else:
            logger.warning(f"The following image does not provide a high enough resolution to be processed by this tool: {path}")
            raise ValueError("Invalid image size!")  
        
        yield config

    except Exception as e:
        logger.error(f"Error in creating the CONFIGURATION object for {path}: {e}")
        logger.info(f"Yield None as config for {path}")
        yield None
