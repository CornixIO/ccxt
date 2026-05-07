import time
from typing import List

from ccxt.mexc_abs import mexc_abs

MEXC_SPOT = 'MEXC Spot'


class mexc_spot(mexc_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'spot'

    def fetch_markets(self, params={}) -> List[dict]:
        return self.fetch_spot_markets(params)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        if since is not None:
            since = int(since)
            until = params.get('until', params.get('endTime', int(time.time() * 1000)))
            params = {**{k: v for k, v in params.items() if k not in ('until', 'endTime')}, 'endTime': int(until)}
        return super().fetch_trades(symbol, since=since, limit=limit, params=params)
