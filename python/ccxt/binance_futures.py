from typing import Any

from ccxt.binance_futures_abs import binance_futures_abs
from ccxt.base.errors import ExchangeError, OrderNotFound
from ccxt.base.types import Str

BINANCE_FUTURES = 'Binance Futures'


class binance_futures(binance_futures_abs):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_futures, self).describe(), {
            'options': {
                'fetchMarkets': ['linear'],
                'defaultType': 'future',
                'defaultSubType': 'linear',
            },
            'exceptions': {
                'linear': {
                    'exact': {
                        '-4400': ExchangeError,
                        '-4401': ExchangeError,
                        '-4402': ExchangeError,
                        '-4403': ExchangeError,
                    }
                },
            }
        })

    def parse_order_status(self, status: Str):
        if status == 'TRIGGERED':
            return 'open'
        return super().parse_order_status(status)

    def fetch_order(self, id: str, symbol: Str = None, params={}):
        if params.get('type') == 'stop' and params.get('clientOrderId'):
            params.pop('type')
            try:
                return super().fetch_order(id, symbol, params)
            except OrderNotFound:
                return super().fetch_order(id, symbol, params | {'stop': True})
        else:
            return super().fetch_order(id, symbol, params)

    def cancel_order(self, id: str, symbol: Str = None, params={}):
        if params.get('type') == 'stop' and params.get('clientOrderId') :
            params.pop('type')
            try:
                return super().cancel_order(id, symbol, params)
            except OrderNotFound:
                return super().cancel_order(id, symbol, params | {'stop': True})
        else:
            return super().cancel_order(id, symbol, params)
