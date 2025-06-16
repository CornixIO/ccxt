from typing import Any

from ccxt.binance import binance

BINANCE = 'Binance'


class binance_spot(binance):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_spot, self).describe(), {
            'options': {
                'fetchMarkets': ['spot'],
                'defaultType': 'spot',
            },
        })

    @staticmethod
    def is_inverse():
        return False

    @staticmethod
    def is_linear():
        return False
