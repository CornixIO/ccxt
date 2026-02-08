from typing import Any

from ccxt.base.errors import ExchangeNotAvailable, PermissionDenied, InvalidNonce
from ccxt.base.types import Str, Int, Market, Order
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

    def parse_order(self, order: dict, market: Market = None) -> Order:
        order_dict = super().parse_order(order, market=market)
        exchange_status = self.safe_string_2(order, 'status', 'ccxtStatus')
        if exchange_status == 'positionIncreaseAtOpenInterestCapRejected':
            order_dict['reject_reason'] = 'exceeds maximum limit allowed'
        return order_dict

    @staticmethod
    def clean_symbol(symbol: Str) -> Any:
        return symbol.split('-')[-1].split(':')[0]

    @staticmethod
    def replace_symbol_k_with_1000(symbol: Str):
        if symbol.startswith('k'):
            stripped_symbol = symbol[1:]
            return f'1000{stripped_symbol}'
        else:
            return symbol

    def coin_to_market_id(self, coin: Str):
        market_id = self.replace_symbol_k_with_1000(coin)
        market_id = super().coin_to_market_id(market_id)
        market_id = self.clean_symbol(market_id)
        return market_id

    def safe_currency_code(self, currency_id, currency=None):
        currency_id = self.replace_symbol_k_with_1000(currency_id)
        return super().safe_currency_code(currency_id)

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
