from typing import List
from ccxt.bingx_abs import bingx_abs
from ccxt.base.types import Market

BINGX_FUTURES = 'BingX Futures'


class bingx_futures(bingx_abs):
    KNOWN_PREFIXES_TO_REMOVE = ['NCSK', 'NCCO', 'NCFX', 'NCSI']

    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.swapV2PrivateGetTradeOrder = self._swapV2PrivateGetTradeOrder

    def fetch_markets(self, params={}) -> List[Market]:
        return self.fetch_swap_markets(params)

    def parse_market(self, market: dict) -> Market:
        from ccxt.bingx_limits import BINGX_LIMITS

        market_obj = super().parse_market(market)
        if market_obj is not None:
            symbol = market_obj['symbol']
            symbol = symbol.replace(':USDT', '').replace(':USDC', '')

            limits = BINGX_LIMITS.get(symbol, {})
            if not limits:
                limits = BINGX_LIMITS.get(market_obj['id'].replace('-', '/'), {})
            market_obj['limits'].update(limits)

            symbol = symbol.replace('2USD/', '/')
            for prefix in self.KNOWN_PREFIXES_TO_REMOVE:
                if symbol.startswith(prefix):
                    symbol = symbol[len(prefix):]
                    break

            market_obj['symbol'] = symbol
        return market_obj

    def _swapV2PrivateGetTradeOrder(self, request):
        if 'clientOrderId' in request:
            request.pop('orderId', None)
        return super().swapV2PrivateGetTradeOrder(request)

    def safe_balance(self, balance):
        for coin, balance_dict in balance.items():
            if coin == 'info':
                continue
            if not balance_dict['free'] and not balance_dict['used']:
                balance_dict['free'] = 0.0
                balance_dict['used'] = 0.0
        return super().safe_balance(balance)
