from typing import List

from ccxt.mexc_abs import mexc_abs

MEXC_FUTURES = 'MEXC Futures'


class mexc_futures(mexc_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'

    def fetch_markets(self, params={}) -> List[dict]:
        markets = self.fetch_swap_markets(params)
        for market in markets:
            symbol = market.get('symbol', '')
            if ':' in symbol:
                market['symbol'] = symbol.split(':')[0]
        return markets
