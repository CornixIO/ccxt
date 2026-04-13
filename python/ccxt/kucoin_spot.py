# -*- coding: utf-8 -*-

from ccxt.kucoin import kucoin
from ccxt.kucoin_abs import KucoinAbs

KUCOIN_SPOT = 'KuCoin'


class kucoin_spot(KucoinAbs, kucoin):
    pass
