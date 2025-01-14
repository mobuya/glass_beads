import cv2
import numpy as np
from find_object import THR_VALUE


'''
Following posts were helpful for creating this function:
https://stackoverflow.com/questions/56604151/how-to-extract-multiple-objects-from-an-image-using-python-opencv
https://stackoverflow.com/questions/64491530/how-to-remove-the-background-from-a-picture-in-opencv-python
https://stackoverflow.com/questions/60989084/python-opencv-crop-image-to-contents-and-make-background-transparent
'''


def place_obj_on_background(images, out_contours, in_contours, transparent, config):
    '''
    Places segmented object(s) onto a single background, either transparent or white, placing them side by side.

    Parameters
    ----------
    images : list of numpy.ndarray
        List of original images containing the beads.

    out_contours : list of numpy.ndarray
        List of outer contours for each object.

    in_contours : list of numpy.ndarray or None
        List of inner contours (holes) for each object, or None if absent.

    transparent : bool
        If True, the background will be transparent; if False, it will be white.

    config : dict
        Configuration dictionary containing padding values.

    Returns
    -------
    canvas: numpy.ndarray
        The combined image with all beads, or one, placed on the background.

    '''
    #TODO: Error handling and logging
    if len(images) != len(out_contours):
        print('paths and contours dont match!')
        return
    
    if len(images) != len(in_contours):
        print('paths and inner contours dont match!') 
        return

    object_sizes = [(cv2.boundingRect(c)[2], cv2.boundingRect(c)[3]) for c in out_contours]
    object_heights = [cv2.boundingRect(c)[3] for c in out_contours]
    object_widths = [cv2.boundingRect(c)[2] for c in out_contours]

    H_PADDING = config["IMG_H_PADDING"]   
    WDTH_PADDING = config["IMG_W_PADDING"]  
    canvas_width = sum(object_widths) + (len(object_widths) - 1) * H_PADDING + 2 * WDTH_PADDING
    canvas_height = max(object_heights) + H_PADDING

    if transparent:
        canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)  
    else:
        canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255  

    
    current_x = WDTH_PADDING
    for img, contour, inner_contour, (w, h) in zip(images, out_contours, in_contours, object_sizes):
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        if inner_contour is not None:
            cv2.drawContours(mask, [inner_contour], -1, 0, thickness=cv2.FILLED)
        extracted_artifact = cv2.bitwise_and(img, img, mask=mask)
         
        x, y, w, h = cv2.boundingRect(contour)
        roi = extracted_artifact[y:y+h, x:x+w]
        cropped_mask = mask[y:y+h, x:x+w]

        if transparent:
            artifact = np.zeros((h, w, 4), dtype=np.uint8)
            artifact[..., :3] = roi
            artifact[..., 3] = cropped_mask
        else:
            artifact = np.ones((h, w, 3), dtype=np.uint8) * 255
            artifact[cropped_mask > 0] = roi[cropped_mask > 0]
        
        h_offset = (canvas_height - h) // 2 
        canvas[h_offset:h_offset + h, current_x:current_x + w] = artifact

        current_x += w + H_PADDING

    return canvas
