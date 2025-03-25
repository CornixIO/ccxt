from ccxt.base.types import Market, Str
from ccxt.hyperliquid import hyperliquid


class hyperliquid_abs(hyperliquid):
    def coin_to_market_id(self, coin: Str):
        market_id = super().coin_to_market_id(coin)
        return market_id.split(':')[0]
