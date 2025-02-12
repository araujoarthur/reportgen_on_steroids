"""
This module defines the SimpleNoPurchaseInPastDays class, which is a specialized report for identifying customers
who have not made a purchase in the past N days. It inherits from the SimpleReport class and implements the 
necessary methods to prepare and execute the query for this specific report.

Classes:
    SimpleNoPurchaseInPastDays: A report class for customers with no purchases in the past N days.
Methods:
    __init__(self, config: dict): Initializes the report with the given configuration.
    prepare_query(self): Prepares the SQL query to be executed for the report.
    feed(self, data: dict): Feeds data into the report and validates the input.
"""

from .simple_report import SimpleReport


class SimpleNoPurchaseInPastDays(SimpleReport):
    """
        Reports customers that didn't purchase in N last days.   
    """

    def __init__(self, config: dict):
        super().__init__(config)
        

      
    def prepare_query(self):
        """
            Prepares tge qyert to be executed
            Child class must implement it to prepare its own query.
        """

        self.query = f"""
            SELECT cliente.CLN_CODIGO AS cliente_codigo,
                            cliente.CLN_NOME AS cliente_nome,
                            CAST(cliente.CLN_DTAULTVND AS DATE) AS data_ultima_venda,
                            cliente.CLN_DTAINS AS cliente_data_cadastro,
                            cliente.CLN_OPEINS AS usuario_cadastro,
                            usuario.usr_nome AS usuario_nome
                FROM cliente
                INNER JOIN usuario ON usuario.usr_login = cliente.cln_opeins
                WHERE cliente.CLN_CODIGO < 500000 AND CAST(cliente.CLN_DTAULTVND AS DATE) < CURRENT_DATE -  { self.query_params[0] };
        """


    def feed(self, data:dict):
        super().feed(data)

        if not data:
            raise Exception("Must pass data")
        
        if not ("days" in data):
            raise Exception("Bad data format")   

        self.query_params = (float(data["days"]),)