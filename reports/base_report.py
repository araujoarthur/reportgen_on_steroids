from typing import Tuple
import os
import pandas as pd
from config.config_manager import Result

type ReportResult = Tuple[bool, int, Exception] 
type DataFrameResult = Tuple[pd.DataFrame, Exception]

class BaseReport:
    def __init__(self):
        self.dataframe = None
        self.query = ""
        self.query_params = None
        self.name = ""
        self.output_path = ""
        self.config = {}

    def generate(self) -> ReportResult:
        """
            Generates the Report
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def feed(data: dict):
        """
            Feeds data into the report generator
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def generate_dataframe(self, rows, columns=None) -> pd.DataFrame:
        """ Generates a Dataframe from the data provided """
        try:
            self.dataframe = pd.DataFrame.from_records(rows, columns=columns)
        except Exception as e:
            return (None, e)
        
        return (self.dataframe, None)
    
    def save_excel_file(self, dataframe: pd.DataFrame) -> Result:
        if not os.path.exists(self.output_path):
            return (False, FileNotFoundError(f"Directory {self.output_path} does not exist"))
        
        filename = f"{self.name}.xlsx"
        filepath = os.path.join(self.output_path, filename)

        try:
            dataframe.to_excel(filepath, index=False)
            return (True, None)            
        except Exception as e:
            return (False, e)