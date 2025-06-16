from typing import Any

from ccxt.binance import binance
from ccxt.base.types import Market

BINANCE_FUTURES = 'Binance Futures'


class binance_futures(binance):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_futures, self).describe(), {
            'options': {
                'fetchMarkets': ['linear'],
                'defaultType': 'future',
            },
        })

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            symbol = market_obj['symbol']
            symbol = symbol.replace(':USDT', '').replace(':USDC', '')
            market_obj['symbol'] = symbol
        return market_obj

    @staticmethod
    def is_inverse(*args, **kwargs):
        return False

    @staticmethod
    def is_linear(*args, **kwargs):
        return True
