from typing import Any

from ccxt.binance_abs import binance_abs

BINANCE_COINS = 'Binance Coin-Futures'


class binance_inverse(binance_abs):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_inverse, self).describe(), {
            'options': {
                'fetchMarkets': ['inverse'],
                'defaultType': 'delivery',
                'defaultSubType': 'inverse',
            },
        })
