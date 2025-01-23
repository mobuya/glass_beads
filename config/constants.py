import numpy as np

'''
MORPH_KERNEL_SIZE: Kernel size for the morphological closing operation.  
MORPH_ITERATIONS: Number of iterations for the closing operation.  
DILATE_KERNEL_SIZE: Kernel size for the dilation operation.  
DILATE_ITERATIONS: Number of iterations for the dilation operation.
MIN_AREA: Minimum contour area to be considered as the artifact (avoid noise).  
INNER_AREA: Minimum area for detecting inner contours (detecting holes in view B).  
MIN_SCALE_AREA: Minimum area required to detect the scale object for pixel-per-metric calculation.  
DILATE_ADAPTATION: Adjustment value for dilation during size prediction to account for contour imperfections. 
IMG_H_PADDING: Horizontal padding added when placing the object on the background.  
IMG_W_PADDING: Vertical padding added when placing the object on the background.  
'''

CONFIGURATION = None

PREDEFINED_CONFIGS = {
    "max_size": {
        "MORPH_KERNEL_SIZE": np.ones((5, 5), np.uint8),
        "MORPH_ITERATIONS": 3,
        "DILATE_KERNEL_SIZE": np.ones((2, 2), np.uint8), 
        "DILATE_ITERATIONS": 1,
        "CLIP_LIMIT": 0.9,
        # find object
        "MIN_AREA": 45000,
        "INNER_AREA": 2900,
        # pixel per metric
        "MIN_SCALE_AREA": 900000,
        # size prediction
        "DILATE_ADAPTATION": 0.2,
        "IMG_H_PADDING": 400, # 400
        "IMG_W_PADDING": 300 # 300
    },
    "min_size": {
        "MORPH_KERNEL_SIZE": np.ones((2, 2), np.uint8),
        "MORPH_ITERATIONS": 1,
        "DILATE_KERNEL_SIZE": np.ones((1, 1), np.uint8),
        "DILATE_ITERATIONS": 0,
        "CLIP_LIMIT": 0.8,
        # find object
        "MIN_AREA": 35000,
        "INNER_AREA": 1000,
        # pixel per metric
        "MIN_SCALE_AREA": 100000,
        # size prediction
        "DILATE_ADAPTATION": 0.2,
        "IMG_H_PADDING": 400,
        "IMG_W_PADDING": 300
    },
}
