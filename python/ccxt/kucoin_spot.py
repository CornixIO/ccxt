# -*- coding: utf-8 -*-

import math
from ccxt.kucoin import kucoin
from ccxt.kucoin_abs import KucoinAbs
from ccxt.base.decimal_to_precision import DECIMAL_PLACES
from ccxt.base.precise import Precise

KUCOIN_SPOT = 'KuCoin'


class kucoin_spot(KucoinAbs, kucoin):
    def describe(self):
        return self.deep_extend(super().describe(), {
            'precisionMode': DECIMAL_PLACES,
            'options': {
                'defaultType': 'spot',
            },
        })

    def fetch_markets(self, params={}):
        markets = super().fetch_markets(params)
        for market in markets:
            info = market.get('info', {})
            precision = market['precision']
            for key, info_key in (('amount', 'baseIncrement'), ('price', 'priceIncrement')):
                val = self.safe_number(info, info_key)
                if val and val > 0:
                    precision[key] = int(round(-math.log10(val))) if val < 1 else 0
            base_min = self.safe_string(info, 'baseMinSize')
            quote_max = self.safe_string(info, 'quoteMaxSize')
            market['limits']['price'] = {
                'min': self.safe_number(info, 'priceIncrement'),
                'max': self.parse_number(Precise.string_div(quote_max, base_min)) if quote_max and base_min else None,
            }
            market['limits']['orders'] = {'max': 200}
            market['limits']['conditional_orders'] = {'max': 20}
        return markets

    def parse_order(self, order, market=None):
        if order and order.get('stop') == '':
            order = {**order, 'stop': None}
        return super().parse_order(order, market)
