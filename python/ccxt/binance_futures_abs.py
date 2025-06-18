from ccxt.binance_abs import binance_abs


class binance_futures_abs(binance_abs):
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
