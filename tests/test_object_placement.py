import unittest
import numpy as np
import cv2

from canvas import place_obj_on_background

class TestPlaceObjOnBackground(unittest.TestCase):

    def setUp(self):
        self.image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        cv2.rectangle(self.image, (30, 30), (70, 70), (0, 0, 0), -1) 

        self.out_contour = np.array([[30, 30], [30, 70], [70, 70], [70, 30]]).reshape((-1, 1, 2))
        self.in_contour = np.array([[40, 40], [40, 60], [60, 60], [60, 40]]).reshape((-1, 1, 2))

        self.config = {
            "IMG_H_PADDING": 10,
            "IMG_W_PADDING": 20
        }

    def test_valid_input(self):
        result = place_obj_on_background([self.image], [self.out_contour], [self.in_contour], transparent=False, config=self.config)
        self.assertIsNotNone(result)

        #three color channels indicate a white background, no transparent
        self.assertEqual(result.shape[2], 3) 

    def test_transparent_output(self):
        result = place_obj_on_background([self.image], [self.out_contour], [self.in_contour], transparent=True, config=self.config)
        self.assertIsNotNone(result)

        # test if background actually transparent
        self.assertEqual(result.shape[2], 4) 

    def test_mismatched_image_and_contours(self):
        result = place_obj_on_background([self.image], [], [], transparent=False, config=self.config)

        #if contour lists and image lists dont match, return none
        self.assertIsNone(result) 

    def test_mismatched_image_and_inn_contours(self):
        result = place_obj_on_background([self.image], [self.out_contour], [], transparent=False, config=self.config)

        #if contour lists and image lists dont match, return none
        self.assertIsNone(result) 

    def test_empty_input(self):
        result = place_obj_on_background([], [], [], transparent=False, config=self.config)

        #tests if the lists are empty, return none
        self.assertIsNone(result) 

    def test_two_objects(self):
        out_contours = [self.out_contour, self.out_contour]

        object_widths =  [cv2.boundingRect(c)[2] for c in out_contours] 
        H_PADDING = self.config["IMG_H_PADDING"]
        WDTH_PADDING = self.config["IMG_W_PADDING"]

        expected_width = (sum(object_widths) + (len(object_widths) - 1) * H_PADDING + 2 * WDTH_PADDING)

        result = place_obj_on_background(
            [self.image, self.image], 
            out_contours, 
            [self.in_contour, self.in_contour], 
            transparent=False, 
            config=self.config
        )

        #should have the proper shape
        self.assertEqual(result.shape[1], expected_width)

    def test_three_objects(self):
        out_contours = [self.out_contour, self.out_contour, self.out_contour]

        object_widths =  [cv2.boundingRect(c)[2] for c in out_contours] 
        H_PADDING = self.config["IMG_H_PADDING"]
        WDTH_PADDING = self.config["IMG_W_PADDING"]

        expected_width = (sum(object_widths) + (len(object_widths) - 1) * H_PADDING + 2 * WDTH_PADDING)

        result = place_obj_on_background(
            [self.image, self.image, self.image], 
            out_contours, 
            [self.in_contour, self.in_contour, self.in_contour], 
            transparent=False, 
            config=self.config
        )

        self.assertEqual(result.shape[1], expected_width)

    def test_output_height(self):
        out_contours = [self.out_contour, self.out_contour, self.out_contour]
        object_heights = [cv2.boundingRect(c)[3] for c in out_contours]

        H_PADDING = self.config["IMG_H_PADDING"]

        expected_height = max(object_heights) + H_PADDING 

        result = place_obj_on_background(
            [self.image, self.image, self.image], 
            [self.out_contour, self.out_contour, self.out_contour], 
            [self.in_contour, self.in_contour, self.in_contour], 
            transparent=False, 
            config=self.config
        )
        self.assertEqual(result.shape[0], expected_height)


if __name__ == '__main__':
    unittest.main()
