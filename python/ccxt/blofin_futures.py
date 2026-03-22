from ccxt.base.precise import Precise
from ccxt.base.types import Market, Num, OrderSide, OrderType
from ccxt.blofin_abs import blofin_abs

BLOFIN_FUTURES = 'BloFin Futures'


class blofin_futures(blofin_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'linear'

    def get_quantity(self, quantity: float, contract_size: float) -> float:
        return float(Precise.string_mul(str(quantity), str(contract_size)))

    def parse_position_tier(self, tier: dict, index: int, market: Market, currency: str) -> dict:
        currency = market['base']
        parsed = super().parse_position_tier(tier, index, market, currency)
        contract_size = market['contractSize']
        if parsed['minNotional'] is not None:
            parsed['minNotional'] = float(Precise.string_mul(str(parsed['minNotional']), str(contract_size)))
        if parsed['maxNotional'] is not None:
            parsed['maxNotional'] = float(Precise.string_mul(str(parsed['maxNotional']), str(contract_size)))
        return parsed

    def create_order_request(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Num = None, params={}):
        order_request = super().create_order_request(symbol, type, side, amount, price, params)
        market = self.market(symbol)
        contractSize = market['contractSize']
        order_request['size'] = Precise.string_div(str(order_request['size']), str(contractSize))
        return order_request
