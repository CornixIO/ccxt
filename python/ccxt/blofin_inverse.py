from ccxt.base.precise import Precise
from ccxt.base.types import Balances, Num, OrderSide, OrderType
from ccxt.blofin_abs import blofin_abs

BLOFIN_INVERSE = 'BloFin Inverse'


class blofin_inverse(blofin_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'inverse'

    def create_order_request(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Num = None, params={}):
        order_request = super().create_order_request(symbol, type, side, amount, price, params)
        market = self.market(symbol)
        contractSize = market['contractSize']
        order_request['size'] = Precise.string_div(str(order_request['size']), str(contractSize))
        return order_request

    def fetch_balance(self, params={}) -> Balances:
        return super().fetch_balance(params | {'accountType': 'inverse_contract'})
