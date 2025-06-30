from typing import Any

from ccxt.base.errors import ExchangeNotAvailable, PermissionDenied, InvalidNonce
from ccxt.base.types import Str, Int
from ccxt.hyperliquid import hyperliquid


class hyperliquid_abs(hyperliquid):
    def describe(self) -> Any:
        return self.deep_extend(super().describe(), {
            'exceptions': {
                'broad': {
                    'User or API Wallet ': PermissionDenied,
                    '502 Server Error': ExchangeNotAvailable,
                    'Invalid nonce': InvalidNonce,
                }
            }
        })

    def parse_order_status(self, status: Str):
        statuses: dict = {
            'positionIncreaseAtOpenInterestCapRejected': 'rejected',
        }
        if parsed_status := statuses.get(status):
            return parsed_status
        return super().parse_order_status(status)

    @staticmethod
    def replace_symbol_k_with_1000(symbol: Str):
        if symbol.startswith('k'):
            stripped_symbol = symbol[1:]
            return f'1000{stripped_symbol}'
        else:
            return symbol

    def coin_to_market_id(self, coin: Str):
        market_id = super().coin_to_market_id(coin)
        market_id = market_id.split(':')[0]
        return self.replace_symbol_k_with_1000(market_id)

    def fetch_order_trades(self, id: str, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        symbol_trades = self.fetch_my_trades(symbol, since, limit, params=params)
        return self.filter_by_array(symbol_trades, 'order', values=[id], indexed=False)

    def fetch_ticker(self, symbol: str, params={}):
        return self.fetch_tickers([symbol])[symbol]

    def replace_k_with_1000(self, markets):
        for market in markets:
            original_symbol = market['symbol']
            market['symbol'] = self.replace_symbol_k_with_1000(original_symbol)
        return markets
