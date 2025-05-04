from ccxt.bingx import bingx


class bingx_abs(bingx):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['broker'] = 'Cornix'

    def is_inverse(self):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'inverse'

    def is_linear(self):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'future'
