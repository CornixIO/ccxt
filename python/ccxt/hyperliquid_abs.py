from typing import Any

from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import PermissionDenied
from ccxt.base.types import Str, Int
from ccxt.hyperliquid import hyperliquid


class hyperliquid_abs(hyperliquid):
    def describe(self) -> Any:
        return self.deep_extend(super().describe(), {
            'exceptions': {
                'broad': {
                    'User or API Wallet ': PermissionDenied,
                    '502 Server Error': ExchangeNotAvailable,
                }
            }
        })

    def coin_to_market_id(self, coin: Str):
        market_id = super().coin_to_market_id(coin)
        return market_id.split(':')[0]

    def fetch_order_trades(self, id: str, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        trades = self.fetch_my_trades(None, since, limit, params=params)
        symbol_to_filter = self.symbol(symbol)
        symbol_trades = self.filter_by_array(trades, 'symbol', values=[symbol_to_filter], indexed=False)
        return self.filter_by_array(symbol_trades, 'order', values=[id], indexed=False)

    def fetch_ticker(self, symbol: str, params={}):
        return self.fetch_tickers([symbol])[symbol]

    @staticmethod
    def replace_k_with_1000(markets):
        for market in markets:
            original_symbol = market['symbol']
            if original_symbol.startswith('k'):
                stripped_symbol = market['symbol'][1:]
                market['symbol'] = f'1000{stripped_symbol}'
                market['original_symbol'] = original_symbol
        return markets

    def symbol(self, symbol):
        market = self.market(symbol)
        return self.safe_string(market, 'original_symbol', symbol) or self.safe_string(market, 'symbol', symbol)
