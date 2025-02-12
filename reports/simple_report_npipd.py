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