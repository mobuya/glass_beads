import unittest
import cv2

from processing import calculate_ppm 
from config import constants

class TestCalculatePPM(unittest.TestCase):


    def test_valid_ppm_calculation_with_image(self):      
        original_image = cv2.imread('tests/scale_test/WITHSCALE_340_020_A.png')

        scale_length = 50

        configuration = constants.PREDEFINED_CONFIGS["max_size"]

        pixel_metric = calculate_ppm(original_image, scale_length, configuration)
        
        self.assertIsNotNone(pixel_metric, "Pixel metric calculation failed")


    def test_ppm_calculation_with_missing_scale(self):
        original_image = cv2.imread('tests/scale_test/NOSCALE_333_006_A.png') 
        
        scale_length = 50
        
        configuration = constants.PREDEFINED_CONFIGS["max_size"]
 
        pixel_metric = calculate_ppm(original_image, scale_length, configuration)
        
        self.assertIsNone(pixel_metric, "Pixel metric should be None when scale is not found")

        
if __name__ == "__main__":
    unittest.main()
