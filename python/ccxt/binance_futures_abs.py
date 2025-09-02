from ccxt.base.errors import ArgumentsRequired, NotSupported
from ccxt.base.types import Int, Str
from ccxt.binance_abs import binance_abs


class binance_futures_abs(binance_abs):
    def handle_leverage_limits(self, leverage_tiers, parsed_market):
        symbol = self.safe_string(parsed_market, 'symbol')
        symbol_position_limits = self.safe_value(leverage_tiers, symbol)
        if symbol_position_limits:
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
            return True
        return False

    def load_markets(self, reload=False, params={}):
        load_leverage = self.safe_string(params, 'load_leverage')
        params = self.omit(params, 'load_leverage')
        parsed_markets = super().load_markets(reload=reload, params=params)
        if load_leverage:
            leverage_tiers = super().fetch_leverage_tiers()

            relevant_markets = dict()
            for parsed_market in parsed_markets.values():
                if self.handle_leverage_limits(leverage_tiers, parsed_market):
                    symbol = self.safe_string(parsed_market, 'symbol')
                    relevant_markets[symbol] = parsed_market
            return relevant_markets
        return parsed_markets

    def set_leverage(self, leverage: Int, symbol: Str = None, params={}):
        """
        set the level of leverage for a market

        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api/Change-Initial-Leverage
        https://developers.binance.com/docs/derivatives/coin-margined-futures/trade/rest-api/Change-Initial-Leverage
        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-UM-Initial-Leverage
        https://developers.binance.com/docs/derivatives/portfolio-margin/account/Change-CM-Initial-Leverage

        :param float leverage: the rate of leverage
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param boolean [params.portfolioMargin]: set to True if you would like to set the leverage for a trading pair in a portfolio margin account
        :returns dict: response from the exchange
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' setLeverage() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
            'leverage': leverage,
        }
        isPortfolioMargin = None
        isPortfolioMargin, params = self.handle_option_and_params_2(params, 'setLeverage', 'papi', 'portfolioMargin', False)
        response = None
        if market['linear']:
            if isPortfolioMargin:
                response = self.papiPostUmLeverage(self.extend(request, params))
            else:
                response = self.fapiPrivatePostLeverage(self.extend(request, params))
        elif market['inverse']:
            if isPortfolioMargin:
                response = self.papiPostCmLeverage(self.extend(request, params))
            else:
                response = self.dapiPrivatePostLeverage(self.extend(request, params))
        else:
            raise NotSupported(self.id + ' setLeverage() supports linear and inverse contracts only')
        return response
