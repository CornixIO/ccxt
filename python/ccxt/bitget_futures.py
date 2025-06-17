from ccxt.bitget_abs import bitget_abs

BITGET_FUTURES = 'Bitget Futures'


class bitget_futures(bitget_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'linear'
