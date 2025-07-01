from typing import Any

from ccxt.binance_futures_abs import binance_futures_abs

BINANCE_COINS = 'Binance Coin-Futures'


class binance_inverse(binance_futures_abs):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_inverse, self).describe(), {
            'options': {
                'fetchMarkets': ['inverse'],
                'defaultType': 'delivery',
                'defaultSubType': 'inverse',
            },
        })
