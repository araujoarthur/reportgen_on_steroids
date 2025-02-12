from typing import Tuple
import os
import pandas as pd
from config.config_manager import Result

type ReportResult = Tuple[bool, int, Exception] 
type DataFrameResult = Tuple[pd.DataFrame, Exception]

class BaseReport:
    """
        BaseReport is an abstract base class for generating reports. It provides
        common functionality and enforces the implementation of specific methods
        in subclasses.

        Attributes:
            dataframe (pd.DataFrame): The dataframe containing the report data.
            query (str): The query string used to fetch data.
            query_params (dict): The parameters for the query.
            name (str): The name of the report.
            output_path (str): The directory path where the report will be saved.
            config (dict): Configuration settings for the report generation.

        Methods:
            generate() -> ReportResult:
                Generates the report. Must be implemented by subclasses.
            feed(data: dict):
                Feeds data into the report generator. Must be implemented by subclasses.
            generate_dataframe(rows, columns=None) -> pd.DataFrame:
                Generates a DataFrame from the provided data.
            save_excel_file(dataframe: pd.DataFrame) -> Result:
                Saves the DataFrame as an Excel file in the specified output path.
    """


    def __init__(self):
        """
            Initializes the base report with default values.

            Attributes:
                dataframe (pd.DataFrame or None): The dataframe to be used in the report.
                query (str): The query string for data extraction.
                query_params (dict or None): The parameters for the query.
                name (str): The name of the report.
                output_path (str): The path where the report will be saved.
                config (dict): Configuration settings for the report.
        """

        self.dataframe = None
        self.query = ""
        self.query_params = None
        self.name = ""
        self.output_path = ""
        self.config = {}


    def generate(self) -> ReportResult:
        """
            Generate the report.
            This method should be implemented by subclasses to generate a report
            and return a ReportResult object.
            
            Raises:
                NotImplementedError: If the method is not implemented by a subclass.
        """
        
        raise NotImplementedError("Subclasses must implement this method.")
    

    def feed(data: dict):
        """
            Abstract method to process and feed data into the report.

            Args:
                data (dict): A dictionary containing the data to be fed into the report.

            Raises:
                NotImplementedError: If the method is not implemented by a subclass.
        """
        
        raise NotImplementedError("Subclasses must implement this method.")


    def generate_dataframe(self, rows, columns=None) -> pd.DataFrame:
        """
            Generates a pandas DataFrame from a list of records.
            
            Args:
                rows (list): A list of records (dictionaries) to be converted into a DataFrame.
                columns (list, optional): A list of column names to use for the DataFrame. Defaults to None.
            
            Returns:
                tuple: A tuple containing the DataFrame and an exception (if any). If the DataFrame is created successfully, 
                    the exception will be None. If an error occurs, the DataFrame will be None and the exception will be returned.
        """
        try:
            self.dataframe = pd.DataFrame.from_records(rows, columns=columns)
        except Exception as e:
            return (None, e)
        
        return (self.dataframe, None)
    

    def save_excel_file(self, dataframe: pd.DataFrame) -> Result:
        """
            Saves the given DataFrame to an Excel file in the specified output path.
            
            Args:
                dataframe (pd.DataFrame): The DataFrame to be saved as an Excel file.
            
            Returns:
                Result: A tuple where the first element is a boolean indicating success (True) or failure (False),
                    and the second element is either None (if successful) or an Exception object (if an error occurred).
            
            Raises:
                FileNotFoundError: If the specified output directory does not exist.
        """

        if not os.path.exists(self.output_path):
            return (False, FileNotFoundError(f"Directory {self.output_path} does not exist"))
        
        filename = f"{self.name}.xlsx"
        filepath = os.path.join(self.output_path, filename)

        try:
            dataframe.to_excel(filepath, index=False)
            return (True, None)            
        except Exception as e:
            return (False, e)