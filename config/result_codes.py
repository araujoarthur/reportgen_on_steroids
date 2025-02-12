from enum import Enum

class ResultCodes(Enum):
    """
    Enum class representing various result codes used throughout the repository.
    Attributes:
        SUCCESS (int): Indicates that the operation was successful.
        NO_QUERY_PROVIDED (int): Indicates that no query was provided for the operation.
        FAILED_TO_CONNECT (int): Indicates that the connection to the database or service failed.
        NO_FILENAME_PROVIDED (int): Indicates that no filename was provided for saving the output.
        FAILED_QUERY (int): Indicates that the query execution failed.
        FAILED_DATAFRAME_GENERATION (int): Indicates that the generation of the DataFrame from the query results failed.
        FAILED_TO_SAVE_EXCEL (int): Indicates that saving the DataFrame to an Excel file failed.
    """

    SUCCESS = 0x0
    NO_QUERY_PROVIDED = 0x1
    FAILED_TO_CONNECT = 0x2
    NO_FILENAME_PROVIDED = 0x3
    FAILED_QUERY = 0x4
    FAILED_DATAFRAME_GENERATION = 0x5
    FAILED_TO_SAVE_EXCEL = 0x6