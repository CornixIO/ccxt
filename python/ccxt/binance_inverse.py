from typing import Any

from ccxt.binancecoinm import binancecoinm

from base.types import Market

BINANCE_COINS = 'Binance Coin-Futures'


class binance_inverse(binancecoinm):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_inverse, self).describe(), {
            'options': {
                'fetchMarkets': ['inverse'],
                'defaultType': 'delivery'
            },
        })

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            symbol = market_obj['symbol']
            symbol = symbol.replace(':USDT', '').replace(':USDC', '')
            market_obj['symbol'] = symbol
        return market_obj