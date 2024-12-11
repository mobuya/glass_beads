import numpy as np

'''
the maximal has 42177408
and the min 2401200

make scenarios for above 40, between 30-40 and 20 -30


this has to be tested with different sizes, minimum is 6000 x 6000

'''

CONFIGURATION = None

PREDEFINED_CONFIGS = {
    "max_size": {
        "MORPH_KERNEL_SIZE": np.ones((5, 5), np.uint8),
        "MORPH_ITERATIONS": 6,
        "DILATE_KERNEL_SIZE": np.ones((5, 5), np.uint8),  # 3 , 3   it = 1
        "DILATE_ITERATIONS": 2,
        # find object
        "MIN_AREA": 45000,
        "INNER_AREA": 2500,
        # pixel per metric
        "MIN_SCALE_AREA": 1000000,
        # size prediction
        "DILATE_ADAPTATION": 0.25,
        "IMG_H_PADDING": 400,
        "IMG_W_PADDING": 300
    },
    "min_size": {
        "MORPH_KERNEL_SIZE": np.ones((5, 5), np.uint8),
        "MORPH_ITERATIONS": 4,
        "DILATE_KERNEL_SIZE": np.ones((2, 2), np.uint8),
        "DILATE_ITERATIONS": 1,
        # find object
        "MIN_AREA": 35000,
        "INNER_AREA": 1000,
        # pixel per metric
        "MIN_SCALE_AREA": 100000,
        # size prediction
        "DILATE_ADAPTATION": 0.2,
         "IMG_H_PADDING": 300,
        "IMG_W_PADDING": 200
    },
}
