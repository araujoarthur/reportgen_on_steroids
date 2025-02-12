"""
This module provides the ConfigManager class, which is responsible for managing the configuration of the application.
It includes methods for retrieving resource paths, creating default configuration files, and loading JSON configuration files.

Classes:
--------
ConfigManager:
    A class that manages the configuration of the application.
    Methods:
    --------
    get_resource_path(relative_path: str) -> str:
        Returns the absolute path to a resource given its relative path, handling both PyInstaller executable and raw script scenarios.
    
    _create_default(dest: str) -> Result:
    
    _load_json(file_path: str) -> ResultDict:
    
    load_configuration(file_path: str) -> ResultDict:
        Loads the configuration from the specified file path. If the configuration file does not exist, it creates a default configuration file.

"""

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
        Manages the configuration of the application.

        Methods
        -------
        get_resource_path(relative_path: str) -> str
            Returns the resource path from a relative path, handling both PyInstaller
            executable and raw script scenarios.

        _create_default(dest: str) -> Result
            Creates the default configuration file in the specified directory.

        _load_json(file_path: str) -> ResultDict
            Loads and parses a JSON configuration file from the given absolute path.

        load_configuration(file_path: str) -> ResultDict
            Loads the configuration from the specified file path. If the configuration
            file does not exist, it creates a default configuration file.
            Manages the configuration of the application
    """

    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        """
            Returns the absolute path to a resource given its relative path.
            This function is useful for accessing resources when the script is 
            packaged as a PyInstaller executable or when running as a raw script.

            Args:
                relative_path (str): The relative path to the resource.

            Returns:
                str: The absolute path to the resource.
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
            Creates the default configuration file in the specified destination directory.
            
            Args:
                dest (str): The destination directory where the default configuration file will be created.
            
            Returns:
                Result: A tuple where the first element is a boolean indicating success (True) or failure (False),
                        and the second element is either None (on success) or an exception object (on failure).
            
            Raises:
                Exception: If an error occurs during the creation of the default configuration file.
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
        Loads a JSON file from the specified file path.
        
        Args:
            file_path (str): The path to the JSON file to be loaded.
        
        Returns:
            ResultDict: A tuple containing the loaded JSON data as a dictionary and an error if any occurred.
                If the file does not exist, returns (None, FileNotFoundError).
                If there is an error during loading, returns (None, Exception).
            
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
        """
            Load the configuration from the specified file path.
            This method checks if the given file path is a file. If it is, it changes the file path to its directory.
            If the directory does not exist, it creates the directory. Then, it constructs the full path to the 
            configuration file. If the configuration file does not exist, it creates a default configuration file.
            Finally, it loads and returns the configuration from the JSON file.
            
            Args:
                file_path (str): The path to the configuration file or directory.
            
            Returns:
                ResultDict: The loaded configuration as a dictionary.
            
            Raises:
                OSError: If there is an error creating the directory or reading the file.
        """

        if os.path.isfile(file_path):
                file_path = os.path.dirname(file_path)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, CONFIG_NAME)
        if not os.path.isfile(file_path) and not os.path.exists(file_path):
            ConfigManager._create_default(os.path.dirname(file_path))
        
        return ConfigManager._load_json(file_path)



    