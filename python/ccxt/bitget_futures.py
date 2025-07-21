from ccxt.bitget_abs import bitget_abs

from ccxt.base.types import Market

BITGET_FUTURES = 'Bitget Futures'


class bitget_futures(bitget_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.options['defaultSubType'] = 'linear'

    def parse_market(self, market) -> Market:
        parsed_market = super().parse_market(market)
        if max_market_order_quantity := market.get('maxMarketOrderQty'):
            parsed_market['limits']['market'] = {
                'max': float(max_market_order_quantity or 0.),
            }
        if max_order_quantity := market.get('maxOrderQty'):
            parsed_market['limits']['amount']['max'] = float(max_order_quantity or 0.)
        return parsed_market
