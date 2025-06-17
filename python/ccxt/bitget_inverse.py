from ccxt.bitget_abs import bitget_abs

BITGET_INVERSE = 'Bitget Inverse'


class bitget_inverse(bitget_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'inverse'
