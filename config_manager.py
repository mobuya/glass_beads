from contextlib import contextmanager
import constants

@contextmanager
def config_context(image_pixels):
    if image_pixels > 35000000:
        config = constants.PREDEFINDED_CONFIGS["max_size"]
    elif image_pixels > 20000000:
        config = constants.PREDEFINDED_CONFIGS["min_size"]
    else:
        raise ValueError("Invalid image size!")

    yield config
