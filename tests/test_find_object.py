import unittest
import cv2

from processing import find_artifact_contour 
from config import constants, HOLE_VIEW, NO_HOLE_VIEW

class TestFindArtifactContour(unittest.TestCase):


    def test_valid_outter_contour_detection(self):      
        original_image = cv2.imread('tests/contour_test/VALID_BEAD_WITH_HOLE.png')

        configuration = constants.PREDEFINED_CONFIGS["max_size"]

        outer_contour, _, _ = find_artifact_contour(original_image, HOLE_VIEW, configuration)

        self.assertIsNotNone(outer_contour, "Outer contour not detected")


    def test_valid_inner_contour_detection(self):      
        original_image = cv2.imread('tests/contour_test/VALID_BEAD_WITH_HOLE.png')

        configuration = constants.PREDEFINED_CONFIGS["max_size"]

        _, inner_contour, _ = find_artifact_contour(original_image, HOLE_VIEW, configuration)

        self.assertIsNotNone(inner_contour, "Inner contour not detected")

    def test_valid_clahe_detection(self):      
        original_image = cv2.imread('tests/contour_test/CLAHE_BEAD.png')

        configuration = constants.PREDEFINED_CONFIGS["max_size"]

        _, _, clahe = find_artifact_contour(original_image, HOLE_VIEW, configuration)

        self.assertTrue(clahe, "CLAHE was not set to true.")


    def test_no_contour_present(self):      
        original_image = cv2.imread('tests/contour_test/NO_BEAD.png')

        configuration = constants.PREDEFINED_CONFIGS["max_size"]

        outer_contour, _, _ = find_artifact_contour(original_image, HOLE_VIEW, configuration)

        self.assertIsNone(outer_contour, "Found a contour on image")


        
if __name__ == "__main__":
    unittest.main()
