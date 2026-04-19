from typing import List

from ccxt.base.precise import Precise
from ccxt.base.types import Market
from ccxt.mexc_abs import mexc_abs

MEXC_FUTURES = 'MEXC Futures'


class mexc_futures(mexc_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'

    def fetch_markets(self, params={}) -> List[dict]:
        markets = self.fetch_swap_markets(params)
        result = []
        for market in markets:
            if not market.get('linear'):
                continue
            symbol = market.get('symbol', '')
            if ':' in symbol:
                market['symbol'] = symbol.split(':')[0]
            contract_size = market.get('contractSize')
            if contract_size:
                limits = market.get('limits', {})
                amount = limits.get('amount', {})
                if amount.get('min') is not None:
                    amount['min'] = amount['min'] * contract_size
                if amount.get('max') is not None:
                    amount['max'] = amount['max'] * contract_size
                precision = market.get('precision', {})
                if precision.get('amount') is not None:
                    precision['amount'] = precision['amount'] * contract_size
            result.append(market)
        return result

    def create_swap_order(self, market, type, side, amount, price=None, marginMode=None, params={}):
        hedged = self.safe_bool(params, 'hedged', False)
        reduceOnly = self.safe_bool(params, 'reduceOnly', False)
        if hedged and reduceOnly:
            params = self.omit(params, 'hedged')
            params = self.extend(params, {'positionMode': 1})
        elif not hedged:
            params = self.extend(params, {'positionMode': 2})
        return super().create_swap_order(market, type, side, amount, price, marginMode, params)

    def parse_position(self, position: dict, market: Market = None):
        position = super().parse_position(position, market)
        info = position['info']

        open_type = str(info.get('openType', '2'))
        margin_type = 'isolated' if open_type == '1' else 'cross'
        position['marginMode'] = margin_type
        position['margin_type'] = margin_type

        position_mode = int(info.get('positionMode', 2))
        is_hedge = position_mode == 1
        position['hedged'] = is_hedge
        position['is_long'] = (position['side'] == 'long') if is_hedge else None

        position['liquidation_price'] = position['liquidationPrice']
        position['maintenance_margin'] = position['initialMargin'] or 0
        position['display_maintenance_margin'] = position['maintenance_margin']

        contracts = position['contracts'] or 0
        quantity = contracts * (1 if position['side'] == 'long' else -1)
        position['quantity'] = quantity

        position['unrealizedPnl'] = float(info.get('unrealizedProfit', 0))

        if position['notional'] is None:
            entry_price = position['entryPrice'] or 0
            position['notional'] = float(
                Precise.string_mul(str(contracts), str(entry_price))
            )

        return position
