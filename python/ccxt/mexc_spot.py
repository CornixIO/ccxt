from ccxt.mexc import mexc

MEXC_SPOT = 'MEXC Spot'


class mexc_spot(mexc):
    def __init__(self, config={}):
        super().__init__(config)
