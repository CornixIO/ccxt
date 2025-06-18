from typing import Any

from ccxt.binance_futures_abs import binance_futures_abs
from ccxt.base.types import Market

BINANCE_FUTURES = 'Binance Futures'


class binance_futures(binance_futures_abs):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_futures, self).describe(), {
            'options': {
                'fetchMarkets': ['linear'],
                'defaultType': 'future',
                'defaultSubType': 'linear',
            },
        })
