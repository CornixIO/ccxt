from typing import Any

from ccxt.binance import binance

BINANCE_FUTURES = 'Binance'


class binance_futures(binance):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_futures, self).describe(), {
            'options': {
                'fetchMarkets': ['spot'],
                'defaultType': 'spot',
            },
        })
