from typing import List
from ccxt.blofin_abs import blofin_abs
from ccxt.base.types import Market

BLOFIN_FUTURES = 'Blofin Futures'


class blofin_futures(blofin_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            symbol = market_obj['symbol'].split(':')[0]
            market_obj['symbol'] = symbol
        return market_obj
