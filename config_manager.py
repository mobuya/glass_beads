from contextlib import contextmanager
import constants
import cv2

@contextmanager
def config_context(path):
    img = cv2.imread(path)
    image_pixels = img.shape[0] * img.shape[1]

    if image_pixels > 35000000:
        config = constants.PREDEFINDED_CONFIGS["max_size"]
    elif image_pixels > 20000000:
        config = constants.PREDEFINDED_CONFIGS["min_size"]
    else:
        raise ValueError("Invalid image size!")

    yield config
