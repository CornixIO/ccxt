from typing import Optional

from ccxt.coinbase import coinbase

COINBASE_ADVANCED_SPOT = 'Coinbase Advanced Spot'


class coinbase_advanced_spot(coinbase):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['fetchBalance'] = 'v3PrivateGetBrokerageAccounts'

    def fetch_order_trades(self, id: str, symbol: Optional[str] = None, since: Optional[int] = None,
                           limit: Optional[int] = None, params={}):
        request = {'order_id': id}
        return self.fetch_my_trades(symbol, since, limit, self.extend(request, params))
