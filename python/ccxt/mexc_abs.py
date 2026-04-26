from ccxt.mexc import mexc
from ccxt.base.errors import DDoSProtection

MEXC = 'MEXC'


class mexc_abs(mexc):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['broker'] = 'CORNIX'
        self.exceptions['exact']['510'] = DDoSProtection  # {"success":false,"code":510,"message":"Requests are too frequent, please try again later"}
