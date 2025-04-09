from typing import List
from ccxt.bingx_abs import bingx_abs
from ccxt.base.types import Market

BINGX_FUTURES = 'BingX Futures'


class bingx_futures(bingx_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'

    def fetch_markets(self, params={}) -> List[Market]:
        return self.fetch_swap_markets(params)

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            market_obj['symbol'] = market_obj['symbol'].replace(':USDT', '')
            market_obj['symbol'] = market_obj['symbol'].replace(':USDC', '')
        return market_obj
