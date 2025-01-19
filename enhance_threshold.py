import cv2


def enhance_and_threshold(image, configuration, threshold_value = 223, CLAHE_BOOL = False):  # thr value is 223
    '''
    Enhances and thresholds an input image to improve contour detection for object segmentation.  
    The function optionally applies Contrast Limited Adaptive Histogram Equalization (CLAHE), followed by thresholding, morphological closing, and dilation to smooth object outline.

    Parameters
    ----------
    image : numpy.ndarray
        The input image.

    configuration : dict
        Dictionary containing kernel sizes and iteration counts for morphological operations.

    threshold_value : int, optional (default=223)
        Threshold value for binary thresholding; pixels below this value are set to 255 (white), and above to 0 (black).

    CLAHE_BOOL : bool, optional (default=False)
        If True, applies CLAHE to enhance image contrast before thresholding.  
        If False, the grayscale image is directly thresholded.

    Returns
    -------
    smooth_outline : numpy.ndarray
        The processed binary image with enhanced and smoothed object contours.  
        White regions represent the detected objects, and black regions represent the background.

    Notes
    -----
    - **CLAHE** is useful for images with uneven lighting or low contrast, useful when artifacts color too similar to background.  
    - **Morphological Closing** closes small gaps in object contours.  
    - **Dilation** smooths object outlines for cleaner segmentation.  
    - IMPORTANT: Proper kernel sizes and iteration counts in `configuration` significantly affect the result.
    '''
    
    MORPH_KERNEL_SIZE = configuration["MORPH_KERNEL_SIZE"]
    MORPH_ITERATIONS = configuration["MORPH_ITERATIONS"]
    DILATE_KERNEL_SIZE = configuration["DILATE_KERNEL_SIZE"]
    DILATE_ITERATIONS = configuration["DILATE_ITERATIONS"]
    CLIP_LIMIT = configuration["CLIP_LIMIT"]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    img = cv2.medianBlur(gray, 5)

    if CLAHE_BOOL:
        clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=(8, 8))   # clahe for full size is 0.9 and 8,8 
        enhanced_image = clahe.apply(img)
        _, threshold_image = cv2.threshold(enhanced_image, threshold_value, 255, cv2.THRESH_BINARY_INV)
    else:   
        _, threshold_image = cv2.threshold(img, threshold_value,255,cv2.THRESH_BINARY_INV)  

    img = cv2.medianBlur(threshold_image, 15)  

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, MORPH_KERNEL_SIZE, iterations=MORPH_ITERATIONS) 
    
    smooth_outline = cv2.dilate(closing, DILATE_KERNEL_SIZE, iterations=DILATE_ITERATIONS)
    
    return smooth_outline
