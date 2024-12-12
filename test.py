import cv2
from config_manager import config_context
import numpy as np
from imutils import perspective
from matplotlib import pyplot as plt
from find_object import get_background_color
from enhance_threshold import enhance_and_threshold

'''
image_path = "invalid_scale.png"
#image_path = "combine_all/ENZFSCH_340_121_B2.png"
#image_path = "MPULDF_005_003_B.png"
template_path = "fitted_color_palette.png"

original_image = cv2.imread(image_path)
bg_col = get_background_color(original_image)

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
template = cv2.imread(template_path,cv2.IMREAD_GRAYSCALE)

img2 = image.copy()
w, h = template.shape[::-1]


best_method = 'TM_CCOEFF_NORMED'  # robust against light and some other invariance 


method = getattr(cv2, best_method)
res = cv2.matchTemplate(img2,template,method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)


cv2.rectangle(original_image, top_left, bottom_right, bg_col, -1)
# cv2.imwrite('no_col.png', original_image)
    



plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle(best_method)

plt.show()
'''
#image_path = "invalid_scale.png"
#image_path = "combine_all/ENZFSCH_340_121_B2.png"
#image_path = "MPULDF_005_003_B.png"
image_path = "combine_all/ENZFSCH_340_191_B.png"

try:
    with config_context(image_path) as config:
        
        #image_path = "combine_all/ENZFSCH_340_121_B2.png"
        #image_path = "MPULDF_005_003_B.png"
        template_path = "fitted_color_palette.png"

        original_image = cv2.imread(image_path)
        bg_col = get_background_color(original_image)

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        template = cv2.imread(template_path,cv2.IMREAD_GRAYSCALE)

        img2 = image.copy()
        w, h = template.shape[::-1]


        best_method = 'TM_CCOEFF_NORMED'  # robust against light and some other invariance 


        method = getattr(cv2, best_method)
        res = cv2.matchTemplate(img2,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)


        cv2.rectangle(original_image, top_left, bottom_right, bg_col, -1)

        threshold_image = enhance_and_threshold(original_image, config, True,  160)

        image_h,_ , _ = original_image.shape

        contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        MIN_SCALE_AREA = config["MIN_SCALE_AREA"]
        scale_contour = None

        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if hierarchy[0][idx][3] == -1 and area > MIN_SCALE_AREA:  #  just look at outer contours
                x, y, w, h = cv2.boundingRect(contour)
                if y > (image_h * 0.5):
                    scale_contour = contour
                    break

        if not (scale_contour is None):
            box = cv2.minAreaRect(scale_contour)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            cv2.drawContours(original_image, [box.astype("int")], -1, (0,255,0), 2)
            cv2.imwrite('detect.png', original_image)
        else:
            print('No scale found, sorry!')

except ValueError as e:
        print(e) 
