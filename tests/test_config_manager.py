import unittest
from unittest.mock import patch, mock_open, MagicMock
from report_generator.config.config_manager import ConfigManager, Result, ResultDict,CONFIG_NAME
import os
import json

class TestConfigManager(unittest.TestCase):

    @patch("config.config_manager.os.path.exists")
    def test_get_resource_path(self, mock_exists):
        """
            Test get_resource_path when running in raw script mode.
        """
        mock_exists.return_value = False
        relative_path = "config/app_config.json"
        expected_path = os.path.join(os.path.abspath("."), relative_path)
        result = ConfigManager.get_resource_path(relative_path)
        self.assertEqual(result, expected_path)
    
    @patch("config.config_manager.shutil.copy")
    @patch("config.config_manager.ConfigManager.get_resource_path")
    def test_create_default_success(self, mock_get_resource_path, mock_copy):
        """
            Test _create_default when it sucessfully creates the default config.
        """
        mock_get_resource_path.return_value = os.path.join("/path/to/source/config/", CONFIG_NAME)
        mock_copy.return_value = None # Mocking the shutil copy function.

        dest_path = os.path.join("/path/to", "destination")
        source_path = os.path.join("/path/to/source", "config", CONFIG_NAME)
        target_path = os.path.join("/path/to/destination", CONFIG_NAME)

        result = ConfigManager._create_default(dest_path)
        self.assertEqual(result, (True, None))
        mock_copy.assert_called_once()
        args, _ = mock_copy.call_args

        self.assertEqual(os.path.normpath(args[0]), os.path.normpath(source_path))
        self.assertEqual(os.path.normpath(args[1]), os.path.normpath(target_path))


    @patch("config.config_manager.os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data='{"key":"value"}')
    def test_load_json_success(self, mock_open_file, mock_exists):
        """
            Test _load_json when the file exists and contains valid JOSN.
        """


        mock_exists.return_value = True
        result = ConfigManager._load_json("/path/to/config.json")
        self.assertEqual(result, ({"key":"value"}, None))
        mock_open_file.assert_called_once_with("/path/to/config.json", 'r')
    
    @patch("config.config_manager.os.path.exists")
    def test_load_json_file_not_found(self, mock_exists):
        """
            Test _load_json when the file does not exist
        """
        mock_exists.return_value = False

        result = ConfigManager._load_json("/path/to/missing_config.json")
        self.assertIsInstance(result[1], FileNotFoundError)
        self.assertEqual(str(result[1]), "Config file not found in:/path/to/missing_config.json")

    
    @patch("config.config_manager.ConfigManager._load_json")
    @patch("config.config_manager.ConfigManager._create_default")
    @patch("config.config_manager.os.path.exists")
    @patch("config.config_manager.os.makedirs")
    def test_load_configuration(self, mock_makedirs, mock_exists, mock_create_default, mock_load_json):
        """Test load_configuration with different conditions."""
        mock_exists.side_effect = [False, False, True]  # Simulate directory missing, then created
        mock_create_default.return_value = (True, None)
        mock_load_json.return_value = ({"key": "value"}, None)
        
        result = ConfigManager.load_configuration("/path/to/config.json")
        self.assertEqual(result, ({"key": "value"}, None))
        mock_makedirs.assert_called_once()
        mock_create_default.assert_called_once()
        mock_load_json.assert_called_once()

if __name__ == "__main__":
    unittest.main()