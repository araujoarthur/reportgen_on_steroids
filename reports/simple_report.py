import os
from .base_report import BaseReport, ReportResult
from db.database import Database
from config.result_codes import ResultCodes

class SimpleReport(BaseReport):
    """
        Base for a simple report that does not manipulate the dataframe.
    """

    def __init__(self, config=None):
        super().__init__()
        self.config = config


    def prepare_query(self):
        """
            Prepares tge qyert to be executed
            Child class must implement it to prepare its own query.
        """
        pass


    def generate(self) -> ReportResult:
        """
            Generates the Report
        """
        db = Database(self.config)
        
        _, err = db.connect()
        if err is not None:
            return (False, ResultCodes.FAILED_TO_CONNECT.value, err)
        
        self.prepare_query()
        if self.query == "":
            return (False, ResultCodes.NO_QUERY_PROVIDED.value, None)
        
        if self.name == "":
            return (False, ResultCodes.NO_FILENAME_PROVIDED.value, None)

        # Executes the query
        res, columns, err = db.execute_query(self.query)
        if err is not None:
            return (False, ResultCodes.FAILED_QUERY.value, err)
        
        # Transforms into a dataframe
        err = None
        res, err = self.generate_dataframe(res, columns)
        if err is not None:
            return (False, ResultCodes.FAILED_DATAFRAME_GENERATION.value, err)

        # Saves to File
        err = None
        res, err = self.save_excel_file(res)
        if err is not None:
            return (False, ResultCodes.FAILED_TO_SAVE_EXCEL.value, err)

        return (True, ResultCodes.SUCCESS.value, None)

    def feed(self, data: dict):
        """
            Feeds data into the report generator.
            Child class must extend it to feed the remaining data.
        """
        if not ("name" in data):
            raise Exception("Must pass a filename")
        
        self.name = data["name"]
        
        self.output_path = data["output_path"] if "output_path" in data else os.path.abspath(".")
        