import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from processing import get_horizontal_dimension

class TestGetHorizontalDimension(unittest.TestCase):
    
    @patch("cv2.minAreaRect")
    @patch("cv2.boxPoints")
    @patch("imutils.perspective.order_points") 
    @patch("scipy.spatial.distance.euclidean")
    def test_valid_contour_with_valid_pixel_metric(self, mock_euclidean, mock_order_points, mock_box_points, mock_min_area_rect):
        pearl_contour = np.array([[[10, 10]], [[10, 20]], [[20, 20]], [[20, 10]]])
        
        mock_min_area_rect.return_value = ((15, 15), (10, 10), 0)
        mock_box_points.return_value = np.array([[10, 10], [20, 10], [20, 20], [10, 20]], dtype="float32")
        mock_order_points.return_value = np.array([[10, 10], [20, 10], [20, 20], [10, 20]], dtype="float32")
        mock_euclidean.return_value = 10.0 

        configuration = {"DILATE_ADAPTATION": 2}

        expected = 8
        result = get_horizontal_dimension(pearl_contour, 1, configuration)

        self.assertEqual(result, expected)

    @patch("cv2.minAreaRect")
    @patch("cv2.boxPoints")
    @patch("imutils.perspective.order_points")
    @patch("scipy.spatial.distance.euclidean")
    def test_no_valid_contour(self, mock_euclidean, mock_order_points, mock_box_points, mock_min_area_rect):
        pearl_contour = None
        mock_euclidean.return_value = 0

        configuration = {"DILATE_ADAPTATION": 2}

        result = get_horizontal_dimension(pearl_contour, 1, configuration)

        self.assertEqual(result, 0.0)

    @patch("cv2.minAreaRect")
    @patch("cv2.boxPoints")
    @patch("imutils.perspective.order_points")
    @patch("scipy.spatial.distance.euclidean")
    def test_no_valid_pixel_metric(self, mock_euclidean, mock_order_points, mock_box_points, mock_min_area_rect):
        pearl_contour = np.array([[[10, 10]], [[10, 20]], [[20, 20]], [[20, 10]]])
        mock_euclidean.return_value = 10.0

        configuration = {"DILATE_ADAPTATION": 2}

        result = get_horizontal_dimension(pearl_contour, None, configuration)

        self.assertEqual(result, 0.0)

if __name__ == "__main__":
    unittest.main()
