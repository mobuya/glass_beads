import cv2
import numpy as np
from enhance_threshold import enhance_and_threshold
from find_object import THR_VALUE


'''

do i need to cite this: https://stackoverflow.com/questions/56604151/how-to-extract-multiple-objects-from-an-image-using-python-opencv ?????

'''


def place_obj_on_background(img_paths, out_contours, in_contours, transparent, config):

    if len(img_paths) != len(out_contours):
        print('paths and contours dont match!')
        return
    
    if len(img_paths) != len(in_contours):
        print('paths and inner contours dont match!')  # some of the inner ones are none, not really good practice but helpful here
        return


    images = [cv2.imread(path) for path in img_paths]
    object_sizes = [(cv2.boundingRect(c)[2], cv2.boundingRect(c)[3]) for c in out_contours]
    object_heights = [cv2.boundingRect(c)[3] for c in out_contours]
    object_widths = [cv2.boundingRect(c)[2] for c in out_contours]

    H_PADDING = config["IMG_H_PADDING"]   
    WDTH_PADDING = config["IMG_W_PADDING"]  
    canvas_width = sum(object_widths) + (len(object_widths) - 1) * H_PADDING + 2 * WDTH_PADDING
    canvas_height = max(object_heights) + H_PADDING

    if transparent:
        canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)  # RGBA for transparency
    else:
        canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255  # White background

    
    current_x = WDTH_PADDING
    for img, contour, inner_contour, (w, h) in zip(images, out_contours, in_contours, object_sizes):
        # no config

        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        if inner_contour is not None:
            cv2.drawContours(mask, [inner_contour], -1, 0, thickness=cv2.FILLED) 
        extracted_artifact = cv2.bitwise_and(img, img, mask=mask)

        # part from old code 
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
        
        h_offset = (canvas_height - h) // 2  # test 
        canvas[h_offset:h_offset + h, current_x:current_x + w] = artifact

        current_x += w + H_PADDING

    return canvas
