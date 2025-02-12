import fdb
import os
from config.config_manager import Result
from typing import Any, Tuple, List

type QueryResult = Tuple[Any, List, Exception]

class Database:
    """
        Class to manage database access
    """
    
    def __init__(self, config:dict):
        """
            Inits the class with the specific database config as a dict.
        """
        self._connection = None
        self.connected = False
        self._config = config
        self.fbclient_lib = os.path.join(os.path.abspath("."),"fbclient.dll")
    
    
    def __del__(self):
        if (not self._connection is None) and (not self._connection.closed):
            self._connection.close()
            
        self._connection = None 
        self.connected = False
    
     
    def connect(self) -> Result:
        """
            Stablishes a connection
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
            Executes a query.
        """ 

        cursor =  self._connection.cursor()
        try:
            cursor.execute(query, params)
            return (cursor.fetchall(), [desc[0] for desc in cursor.description], None)
        except Exception as e:
            return (None, 0, e)
        
    
