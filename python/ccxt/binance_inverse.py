from ccxt.binancecoinm import binancecoinm

BINANCE_COINS = 'Binance Coin-Futures'


class binance_inverse(binancecoinm):
    def describe(self) -> Any:
        return self.deep_extend(super(binance_futures, self).describe(), {
            'options': {
                'fetchMarkets': ['inverse'],
                'defaultType': 'delivery'
            },
        })
