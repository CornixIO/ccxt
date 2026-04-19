from typing import List

from ccxt.base.precise import Precise
from ccxt.base.types import Market
from ccxt.base.errors import OrderNotFound
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
                contract_size = str(contract_size)
                if amount.get('min') is not None:
                    amount['min'] = float(Precise.string_mul(str(amount['min']), contract_size))
                if amount.get('max') is not None:
                    amount['max'] = float(Precise.string_mul(str(amount['max']), contract_size))
                precision = market.get('precision', {})
                if precision.get('amount') is not None:
                    precision['amount'] = float(Precise.string_mul(str(precision['amount']), contract_size))
                info = market.get('info', {})
                risk_limit_custom = self.safe_value(info, 'riskLimitCustom', [])
                if risk_limit_custom:
                    limits['risk'] = [
                        {
                            'id': self.safe_integer(tier, 'level'),
                            'limit': float(Precise.string_mul(str(self.safe_number(tier, 'maxVol')), contract_size)),
                            'max_leverage': self.safe_integer(tier, 'maxLeverage'),
                        }
                        for tier in risk_limit_custom
                    ]
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
        contract_size = market.get('contractSize')
        if contract_size:
            amount = float(Precise.string_div(str(amount), str(contract_size)))
        trigger_price = self.safe_number_2(params, 'triggerPrice', 'stopPrice')
        if trigger_price:
            if type == 'market':
                params = self.extend(params, {'orderType': 5})
            if 'triggerType' not in params:
                params = self.extend(params, {'triggerType': 2 if side == 'sell' else 1})
        return super().create_swap_order(market, type, side, amount, price, marginMode, params)

    def fetch_order(self, id: str, symbol=None, params={}):
        if not self.safe_bool(params, 'stop', False):
            return super().fetch_order(id, symbol, params)
        if symbol is None:
            raise OrderNotFound(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        plan_response = self.contractPrivateGetPlanorderListOrders({'symbol': market['id']})
        for order in self.safe_value(plan_response, 'data', []):
            if self.safe_string(order, 'id') == str(id):
                return self.parse_order(order, market)
        raise OrderNotFound(self.id + ' fetchOrder() plan order not found: ' + str(id))

    def parse_order(self, order: dict, market: Market = None):
        parsed = super().parse_order(order, market)
        symbol = parsed.get('symbol')
        if symbol:
            market_data = self.safe_value(self.markets, symbol, {})
            contract_size = market_data.get('contractSize')
            if contract_size:
                contract_size_str = str(contract_size)
                if parsed.get('amount') is not None:
                    parsed['amount'] = float(Precise.string_mul(str(parsed['amount']), contract_size_str))
                if parsed.get('filled') is not None:
                    parsed['filled'] = float(Precise.string_mul(str(parsed['filled']), contract_size_str))
        info = parsed.get('info') or {}
        if info.get('triggerPrice') is not None:
            order_type_int = self.safe_integer(info, 'orderType')
            parsed['type'] = 'market' if order_type_int == 5 else 'limit'
            side_int = self.safe_integer(info, 'side')
            parsed['side'] = 'buy' if side_int in (1, 2) else 'sell'
            state_map = {'1': 'open', '2': 'closed', '3': 'canceled', '4': 'canceled'}
            parsed['status'] = state_map.get(str(self.safe_integer(info, 'state')), parsed.get('status'))
            parsed['reduceOnly'] = self.safe_bool(info, 'reduceOnly', False)
        return parsed

    def parse_trade(self, trade: dict, market: Market = None):
        parsed = super().parse_trade(trade, market)
        symbol = parsed.get('symbol')
        if symbol:
            market_data = self.safe_value(self.markets, symbol, {})
            contract_size = market_data.get('contractSize')
            if contract_size:
                contract_size_str = str(contract_size)
                if parsed.get('amount') is not None:
                    parsed['amount'] = float(Precise.string_mul(str(parsed['amount']), contract_size_str))
        return parsed

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
