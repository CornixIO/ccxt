from ccxt.bitget import bitget


class bitget_inverse(bitget):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'inverse'
