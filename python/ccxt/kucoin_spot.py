# -*- coding: utf-8 -*-

from ccxt.kucoin import kucoin
from ccxt.kucoin_abs import KucoinAbs

KUCOIN_SPOT = 'KuCoin'


class kucoin_spot(KucoinAbs, kucoin):
    def describe(self):
        return self.deep_extend(super().describe(), {
            'options': {
                'defaultType': 'spot',
            },
        })

    def parse_order(self, order, market=None):
        if order and order.get('stop') == '':
            order = {**order, 'stop': None}
        return super().parse_order(order, market)

    def fetch_markets(self, params={}):
        markets = super().fetch_markets(params)
        for market in markets:
            precision = market.get('precision') or {}
            for key in ('amount', 'price'):
                val = precision.get(key)
                if isinstance(val, int) and val > 0:
                    precision[key] = 10 ** -val
        return markets
