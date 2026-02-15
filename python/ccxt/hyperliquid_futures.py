from typing import List

from ccxt.base.types import Market
from ccxt.hyperliquid_abs import hyperliquid_abs

HYPERLIQUID_FUTURES = 'HyperLiquid Futures'


class hyperliquid_futures(hyperliquid_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'

    def fetch_markets(self, params={}) -> List[Market]:
        markets = self.fetch_swap_markets(params) + self.fetch_hip3_markets(params)
        relevant_markets = []
        for market in markets:
            symbol = self.clean_symbol(market['symbol'])
            market['symbol'] = symbol
            if symbol.endswith('/USDC'):
                relevant_markets.append(market)
        relevant_markets = self.replace_k_with_1000(relevant_markets)
        return relevant_markets
