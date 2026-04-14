from ccxt.base.precise import Precise
from ccxt.base.types import Market
from ccxt.mexc import mexc

MEXC = 'MEXC'


class mexc_abs(mexc):
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
