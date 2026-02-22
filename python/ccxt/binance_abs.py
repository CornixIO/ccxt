from typing import Any

from ccxt.base.decimal_to_precision import DECIMAL_PLACES, ROUND
from ccxt.base.errors import ArgumentsRequired, BadRequest, BadSymbol
from ccxt.base.types import Int, Market, MarketInterface, Str, Strings
from ccxt.binance import binance

PERMISSION_TO_VALUE = {"spot": ["enableSpotAndMarginTrading"], "futures": ["enableFutures"],
                       "withdrawal": ["enableWithdrawals"]}


class binance_abs(binance):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_abs, self).describe(), {
            'precisionMode': DECIMAL_PLACES,
            'options': {'broker': {
                'spot': 'x-MLHZG2J2',
                'margin': 'x-MLHZG2J2',
                'future': 'x-v69H3rG1',
                'swap': 'x-v69H3rG1',
                'delivery': 'x-sDPWvduU',
                'option': 'x-sDPWvduU',
                'inverse': 'x-sDPWvduU',
            }}
        })

    def get_broker_id(self):
        broker = self.safe_dict(self.options, 'broker', {})
        return self.safe_string(broker, self.options['defaultType'])

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
        try:
            return super().market(symbol)
        except Exception:
            raise BadSymbol(self.id + ' does not have market symbol ' + symbol)

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
                'amount': self.safe_integer_2(market, 'quantityPrecision', 'quantityScale'),
                'price': self.safe_integer_2(market, 'pricePrecision', 'priceScale'),
            }

            if 'PRICE_FILTER' in filters_by_type:
                _filter = self.safe_value(filters_by_type, 'PRICE_FILTER', {})
                precision['price'] = self.precision_from_string(_filter['tickSize'])
            if 'LOT_SIZE' in filters_by_type:
                _filter = self.safe_value(filters_by_type, 'LOT_SIZE', {})
                step_size = self.safe_string(_filter, 'stepSize')
                precision['amount'] = self.precision_from_string(step_size)
            parsed_market['precision'] = precision
        return parsed_market

    def fetch_order_trades(self, id: str, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrderTrades() requires a symbol argument')
        self.load_markets()
        params = self.omit(params, 'type')
        request: dict = {
            'orderId': id,
        }
        return self.fetch_my_trades(symbol, since, limit, self.extend(request, params))

    def market_symbols(self, symbols: Strings = None, type: Str = None, allowEmpty=True, sameTypeOnly=False, sameSubTypeOnly=False):
        if symbols is None:
            if not allowEmpty:
                raise ArgumentsRequired(self.id + ' empty list of symbols is not supported')
            return symbols
        symbolsLength = len(symbols)
        if symbolsLength == 0:
            if not allowEmpty:
                raise ArgumentsRequired(self.id + ' empty list of symbols is not supported')
            return symbols
        result = []
        marketType = None
        isLinearSubType = None
        for i in range(0, len(symbols)):
            market = self.market(symbols[i])
            if sameTypeOnly and (marketType is not None):
                if market['type'] != marketType:
                    raise BadRequest(self.id + ' symbols must be of the same type, either ' + marketType + ' or ' + market['type'] + '.')
            if sameSubTypeOnly and (isLinearSubType is not None):
                if market['linear'] != isLinearSubType:
                    raise BadRequest(self.id + ' symbols must be of the same subType, either linear or inverse.')
            if type is not None and market['type'] != type:
                raise BadRequest(self.id + ' symbols must be of the same type ' + type + '. If the type is incorrect you can change it in options or the params of the request')
            marketType = market['type']
            if not market['spot']:
                isLinearSubType = market['linear']
            symbol = self.safe_string(market, 'symbol', symbols[i])
            result.append(symbol)
        return result

    def get_market_from_symbols(self, symbols: Strings = None):
        if symbols is None:
            return None
        firstMarket = self.safe_string(symbols, 0)
        market = self.market(firstMarket)
        return market
