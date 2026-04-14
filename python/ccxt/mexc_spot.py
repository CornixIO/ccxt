from typing import List

from ccxt.mexc import mexc

MEXC_SPOT = 'MEXC Spot'


class mexc_spot(mexc):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'spot'

    def fetch_markets(self, params={}) -> List[dict]:
        return self.fetch_spot_markets(params)
