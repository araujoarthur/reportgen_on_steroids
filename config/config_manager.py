import os
import sys
import shutil
from typing import Tuple, Dict
import json

type Result = Tuple[bool, Exception]
type ResultDict = Tuple[Dict, Exception]

CONFIG_NAME = "app_config.json"


class ConfigManager:
    """
        Manages the configuration of the application
    """

    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        """
            Returns the a resource path from a relative path
        """
        if hasattr(sys, "_MEIPASS"):
            # Returns the path if running as a PyInstaller freezed' executable
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # Returns the path if running as a raw script
            return os.path.join(os.path.abspath("."), relative_path)
    


    @staticmethod
    def _create_default(dest: str) -> Result:
        """
            Creates the default config in the executable directory.
        """
        try:
            target_path = os.path.join(dest, CONFIG_NAME)
        
            source_path = ConfigManager.get_resource_path(os.path.join("config", CONFIG_NAME))
            shutil.copy(source_path, target_path)
            return (True, None)
        except Exception as e:
            return (False, e)
        
    
    @staticmethod
    def _load_json(file_path: str) -> ResultDict:
        """
            Loads the JSON from an absolute path
        """
        if not os.path.exists(file_path):
            return (None, FileNotFoundError(f"Config file not found in:{file_path}"))
        
        json_data = dict()
        with open(file_path, 'r') as f:
            try:
                json_data = json.load(f)
                return (json_data, None)
            except Exception as e:
                return (None, e)
        

    @staticmethod
    def load_configuration(file_path: str) -> ResultDict:
        if os.path.isfile(file_path):
                file_path = os.path.dirname(file_path)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, CONFIG_NAME)
        if not os.path.isfile(file_path) and not os.path.exists(file_path):
            ConfigManager._create_default(os.path.dirname(file_path))
        
        return ConfigManager._load_json(file_path)



    