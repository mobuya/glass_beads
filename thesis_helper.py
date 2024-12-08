import cv2
from config_manager import config_context
from enhance_threshold import enhance_and_threshold
from find_object import find_artifact_contour_and_color

path = 'ENZFSCH_340_022_A.png'
image = cv2.imread(path)

try:
    with config_context(36000000) as config:
        contour, _, _ = find_artifact_contour_and_color(path, 'X', config)
        cv2.drawContours(image, [contour], -1, (0,0,255), 15)
        cv2.imwrite('outline.png', image)
except ValueError as e:
    print(e)

