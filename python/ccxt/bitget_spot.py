from ccxt.bitget_abs import bitget_abs

BITGET_SPOT = 'Bitget Spot'


class bitget_spot(bitget_abs):
    def __init__(self, config={}):
        super().__init__(config)
