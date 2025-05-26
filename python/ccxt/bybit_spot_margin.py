from ccxt.bybit import bybit


class bybit_spot_margin(bybit):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'spot'

    def set_leverage(self, symbol, leverage=None, long_leverage=None, short_leverage=None, params={}):
        """
        set the level of leverage for a market

        https://bybit-exchange.github.io/docs/v5/spot-margin-uta/set-leverage

        :param str leverage: the rate of leverage
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: response from the exchange
        """
        self.load_markets()
        leverageString = self.number_to_string(leverage)
        request: dict = {
            'leverage': leverageString,
        }
        response = self.privatePostV5SpotMarginTradeSetLeverage(self.extend(request, params))
        return response

    def fetch_spot_markets(self, params):
        markets = super().fetch_spot_markets(params)
        margin_markets = list()
        for market in markets:
            info = market['info']
            is_margin = info.get('marginTrading') != 'none'
            if is_margin:
                market['margin'] = True
                margin_markets.append(market)
        return margin_markets
