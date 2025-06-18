from typing import Any

from ccxt.base.errors import BadSymbol
from ccxt.base.types import Market, MarketInterface
from ccxt.binance import binance
from ccxt.base.decimal_to_precision import ROUND, DECIMAL_PLACES

PERMISSION_TO_VALUE = {"spot": ["enableSpotAndMarginTrading"], "futures": ["enableFutures"],
                       "withdrawal": ["enableWithdrawals"]}


class binance_abs(binance):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_abs, self).describe(), {
            'precisionMode': DECIMAL_PLACES,
        })

    def is_inverse(self, *args, **kwargs):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'delivery'

    def is_linear(self, *args, **kwargs):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'future'

    def get_api_account_details(self):
        response = self.sapi_get_account_apirestrictions()
        permissions = self.extract_trading_permissions(PERMISSION_TO_VALUE, response=response)
        return {
            'info': response,
            "creation": self.safe_integer(response, "createTime"),
            "expiration": self.safe_integer(response, "tradingAuthorityExpirationTime"),
            "permissions": permissions,
            "ip_restrict": self.safe_value(response, "ipRestrict")
        }

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, ROUND, self.markets[symbol]['precision']['price'], self.precisionMode)

    def market(self, symbol: str | None) -> MarketInterface:
        if symbol is None:
            raise BadSymbol(self.id + ' does not have market symbol None')
        return super().market(symbol)

    def parse_market(self, market: dict) -> Market:
        parsed_market = super().parse_market(market)
        if parsed_market is not None:
            symbol = parsed_market['id'] if parsed_market['future'] else parsed_market['symbol'].split(':')[0]
            parsed_market['symbol'] = symbol

            filters = self.safe_list(market, 'filters', [])
            filters_by_type = self.index_by(filters, 'filterType')

            if 'MAX_NUM_ORDERS' in filters_by_type:
                _filter = self.safe_value(filters_by_type, 'MAX_NUM_ORDERS', {})
                max_num_orders = self.safe_float(_filter, 'maxNumOrders')
                if not max_num_orders:
                    max_num_orders = self.safe_float(_filter, 'limit')
                parsed_market['limits']['orders'] = {'max': max_num_orders}
            if 'MAX_NUM_ALGO_ORDERS' in filters_by_type:
                _filter = self.safe_value(filters_by_type, 'MAX_NUM_ALGO_ORDERS', {})
                max_num_algo_orders = self.safe_float(_filter, 'maxNumAlgoOrders')
                if not max_num_algo_orders:
                    max_num_algo_orders = self.safe_float(_filter, 'limit')
                parsed_market['limits']['conditional_orders'] = {'max': max_num_algo_orders}
            parsed_market['limits']['exchange_total_orders'] = {'max': 1000}

            precision = {
                'base': self.safe_integer(market, 'baseAssetPrecision'),
                'quote': self.safe_integer(market, 'quotePrecision'),
                'amount': self.safe_string_2(market, 'quantityPrecision', 'quantityScale'),
                'price': self.safe_string_2(market, 'pricePrecision', 'priceScale'),
            }

            if precision.get('price') is None and 'PRICE_FILTER' in filters_by_type:
                _filter = self.safe_value(filters_by_type, 'PRICE_FILTER', {})
                precision['price'] = self.precision_from_string(_filter['tickSize'])
            if precision.get('amount') is None and 'LOT_SIZE' in filters_by_type:
                _filter = self.safe_value(filters_by_type, 'LOT_SIZE', {})
                step_size = self.safe_string(_filter, 'stepSize')
                precision['amount'] = self.precision_from_string(step_size)
            parsed_market['precision'] = precision
        return parsed_market
