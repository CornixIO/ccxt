from ccxt.mexc import mexc

MEXC = 'MEXC'


class mexc_abs(mexc):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['broker'] = 'CORNIX'
