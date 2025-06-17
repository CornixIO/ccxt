from typing import Any

from ccxt.binance_abs import binance_abs

BINANCE = 'Binance'


class binance_spot(binance_abs):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_spot, self).describe(), {
            'options': {
                'fetchMarkets': ['spot'],
                'defaultType': 'spot',
            },
        })
