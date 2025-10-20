from ccxt.blofin import blofin


class blofin_abs(blofin):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['broker'] = 'Cornix'
