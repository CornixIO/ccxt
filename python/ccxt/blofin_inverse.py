from ccxt.base.precise import Precise
from ccxt.base.types import Balances, Num, OrderSide, OrderType
from ccxt.blofin_abs import blofin_abs

BLOFIN_INVERSE = 'BloFin Inverse'


class blofin_inverse(blofin_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'inverse'

    def fetch_balance(self, params={}) -> Balances:
        return super().fetch_balance(params | {'accountType': 'inverse_contract'})
