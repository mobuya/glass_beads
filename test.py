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

image_path = "combine_all/ENZFSCH_340_138_A.png"

'''
clahe works with pearls, that have a nice bright image, didnt trry it with other normal colored pearls, but with darker images it wont work, 
oopsie, 
gotta see how it works wit the rest to determine if i should implement it with clahe or not
'''

try:
    with config_context(image_path) as config:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        clahe = cv2.createCLAHE(clipLimit=0.7, tileGridSize=(3, 3))

        enhanced_image = clahe.apply(image)

        _, binary = cv2.threshold(enhanced_image, 223, 255, cv2.THRESH_BINARY_INV)

      
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # Draw the contours for visualization
        print(len(contours))
        for c in contours:
             if cv2.contourArea(c) > 2500:
                cv2.drawContours(output, [c], -1, (0, 255, 0), 2)
        
        cv2.imwrite('test_ccmp.png', output)

except ValueError as e:
        print(e) 
