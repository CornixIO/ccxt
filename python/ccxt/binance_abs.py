from ccxt.base.errors import BadSymbol
from ccxt.base.types import Market, MarketInterface
from ccxt.binance import binance

PERMISSION_TO_VALUE = {"spot": ["enableSpotAndMarginTrading"], "futures": ["enableFutures"],
                       "withdrawal": ["enableWithdrawals"]}


class binance_abs(binance):
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

    def market(self, symbol: str | None) -> MarketInterface:
        if symbol is None:
            raise BadSymbol(self.id + ' does not have market symbol None')
        return super().market(symbol)

    def handle_leverage_limits(self, leverage_tiers, parsed_market):
        symbol = self.safe_string(parsed_market, 'symbol')
        symbol_position_limits = self.safe_value(leverage_tiers, symbol)
        position_limits = []
        last_max_leverage = 0.
        for symbol_leverage_limit in sorted(symbol_position_limits, key=lambda x: x['maxLeverage']):
            max_leverage = self.safe_float(symbol_leverage_limit, 'maxLeverage')
            max_position_size = self.safe_float(symbol_leverage_limit, "maxNotional")
            result = {'max_leverage': max_leverage, 'limit': max_position_size}
            position_limits.append(result)

            last_max_leverage = max_leverage

        parsed_market['limits']['leverage'] = {'max': last_max_leverage}
        parsed_market['limits']['risk'] = position_limits

    def load_markets(self, reload=False, params={}):
        parsed_markets = super().load_markets(reload=reload, params=params)
        if getattr(self, '_should_load_leverage_tiers', True):
            self._should_load_leverage_tiers = False
            try:
                leverage_tiers = super().fetch_leverage_tiers()
            finally:
                self._should_load_leverage_tiers = True

            for parsed_market in parsed_markets.values():
                self.handle_leverage_limits(leverage_tiers, parsed_market)
        return parsed_markets

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
        return parsed_market
