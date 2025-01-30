import unittest
from unittest.mock import patch, MagicMock
import cv2
from config import config_context, constants


class TestConfigContext(unittest.TestCase):
    
    @patch("cv2.imread")
    def test_valid_large_image(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(6000, 6000, 3))
        
        with config_context("test_large_image.jpg") as config:
            self.assertEqual(config, constants.PREDEFINED_CONFIGS["max_size"])

    @patch("cv2.imread")
    def test_valid_medium_image(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(5000, 4500, 3))
        
        with config_context("test_medium_image.jpg") as config:
            self.assertEqual(config, constants.PREDEFINED_CONFIGS["min_size"])

    @patch("cv2.imread")
    def test_invalid_image_too_small(self, mock_imread):
        mock_imread.return_value = MagicMock(shape=(1000, 1000, 3))
        
        with config_context("test_small_image.jpg") as config:
            self.assertIsNone(config)  

    @patch("cv2.imread")
    def test_image_not_found(self, mock_imread):
        mock_imread.return_value = None
        
        with config_context("non_existent_image.jpg") as config:
            self.assertIsNone(config)

    @patch("cv2.imread")
    def test_error_handling_in_context(self, mock_imread):
        mock_imread.side_effect = Exception("Some error")
        
        with config_context("test_error_image.jpg") as config:
            self.assertIsNone(config)  

if __name__ == "__main__":
    unittest.main()
