import fdb
import os
from config.config_manager import Result
from typing import Any, Tuple, List

type QueryResult = Tuple[Any, List, Exception]

# TO-DO: Switch to firebird-driver https://pypi.org/project/firebird-driver/
class Database:
    """
        Class to manage database access.

        Attributes:
            _connection (fdb.Connection): The connection object to the database.
            connected (bool): A flag indicating whether the database is connected.
            _config (dict): The configuration dictionary for the database connection.
            fbclient_lib (str): The path to the Firebird client library.
        
        Methods:
            __init__(config: dict):
                Initializes the Database class with the specified configuration.
            __del__():
                Destructor that ensures the database connection is closed.
            connect() -> Result:
                Establishes a connection to the database.
            execute_query(query: str, params: Optional[tuple] = None) -> QueryResult:
                Executes a query on the database.
    """

    
    def __init__(self, config:dict):
        """
        Initializes the database connection class with the specified configuration.

        Args:
            config (dict): A dictionary containing the database configuration parameters.

        Attributes:
            _connection (None): Placeholder for the database connection object.
            connected (bool): Flag indicating whether the database is connected.
            _config (dict): Stores the database configuration parameters.
            fbclient_lib (str): Path to the Firebird client library.
        """

        self._connection = None
        self.connected = False
        self._config = config
        self.fbclient_lib = os.path.join(os.path.abspath("."),"fbclient.dll")
    
    
    def __del__(self):
        """
            Destructor method that ensures the database connection is properly closed 
            when the instance is being destroyed. If the connection is open, it closes 
            the connection and sets the connection attributes to None and False.
        """
        if (not self._connection is None) and (not self._connection.closed):
            self._connection.close()
            
        self._connection = None 
        self.connected = False
    
     
    def connect(self) -> Result:
        """
            Establishes a connection to the Firebird database using the configuration
            provided in the instance's _config attribute.

            Returns:
                Result: A tuple where the first element is a boolean indicating the 
                success of the connection attempt, and the second element is either 
                None (if the connection was successful) or an exception object (if 
                an error occurred).

            Raises (check on return):
                fdb.DatabaseError: If there is an error related to the database.
                fdb.ProgrammingError: If there is a programming error.
                Exception: For any other exceptions that may occur.
        """
        
        try:
            self._connection = fdb.connect(
                host=self._config["host"],
                port = self._config["port"],
                database= self._config["path"],
                user=self._config["username"],
                password=self._config["password"],
                fb_library_name=self.fbclient_lib
            )
            self.connected = True
            return (True, None)
        except fdb.DatabaseError as e:
            return (False, e)
        except fdb.ProgrammingError as e:
            return (False, e)
        except Exception as e:
            return (False, e)
    

    def execute_query(self, query, params=None) -> QueryResult:
        """
            Executes a SQL query on the database.
            
            Args:
                query (str): The SQL query to be executed.
                params (tuple, optional): The parameters to be used with the SQL query. Defaults to None.
            
            Returns:
                QueryResult: A tuple containing:
                - list: The fetched results from the query.
                - list: The column names of the fetched results.
                - Exception: An exception object if an error occurred, otherwise None.            
        """ 

        cursor =  self._connection.cursor()
        try:
            cursor.execute(query, params)
            return (cursor.fetchall(), [desc[0] for desc in cursor.description], None)
        except Exception as e:
            return (None, 0, e)
        
    
