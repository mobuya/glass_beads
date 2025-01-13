import cv2
from config_manager import config_context
import numpy as np
from imutils import perspective
from matplotlib import pyplot as plt
from find_object import get_background_color
from enhance_threshold import enhance_and_threshold


#image_path = "combine_all/ENZFSCH_340_015_A.png"

#image_path = "combine_all/ENZFSCH_340_191_B.png"

#image_path = "combine_all/ENZFSCH_333_026_B.png"

#image_path = "combine_all/ENZFSCH_340_138_A.png"
#image_path = "combine_all/ENZFSCH_340_017_B1.png"

#image_path = "combine_all/ENZFSCH_340_117_B2.png"

image_path = "upload_images/ENZFSCH_333_009_A.png"
'''
clahe works with pearls, that have a nice bright image, didnt trry it with other normal colored pearls, but with darker images it wont work, 
oopsie, 
gotta see how it works wit the rest to determine if i should implement it with clahe or not
'''

try:
    with config_context(image_path) as config:
        image = cv2.imread(image_path)

        thr_img = enhance_and_threshold(image, config, False, threshold_value=180)

        contours, _ = cv2.findContours(thr_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
             if cv2.contourArea(c) > 2500:
                rect = cv2.boundingRect(c)
                x,y,w,h = rect
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),10)
                cv2.drawContours(image, [c], -1, (255, 0, 0), 5)

        cv2.imwrite('test_bool.png', image)

except ValueError as e:
        print(e) 
