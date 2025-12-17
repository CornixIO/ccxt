from typing import Any, List, Optional

from ccxt.base.errors import OrderNotFound
from ccxt.base.precise import Precise
from ccxt.base.types import Market, Order, Str
from ccxt.blofin import blofin


class blofin_abs(blofin):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['brokerId'] = '3c336d82b979ebd1'

    def describe(self) -> Any:
        return self.deep_extend(super().describe(), {
            'api': {
                'private': {
                    'get': {
                        'trade/order-detail': 1,
                        'trade/order-tpsl-detail': 1,
                    },
                },
            },
        })

    def get_quantity(self, quantity: float, contract_size: float) -> float:
        return quantity

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            info = market_obj['info']
            market_obj['symbol'] = market_obj['symbol'].split(':')[0]
            contract_size = float(market_obj['contractSize'])
            limits = market_obj['limits']
            limits['amount']['max'] = self.get_quantity(float(info['maxLimitSize']), contract_size)
            limits['market'] = {'min': 0., 'max': self.get_quantity(float(info['maxMarketSize']), contract_size)}
            market_obj['precision']['amount'] = self.get_quantity(float(market_obj['precision']['amount']), contract_size)
            contract_type = info['contractType']
            market_obj['linear'] = contract_type == 'linear'
            market_obj['inverse'] = contract_type == 'inverse'
        return market_obj

    def get_trade_order_detail(self, symbol: Str = None, params={}) -> Order:
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'instId': market['id'],
        }
        response = self.privateGetTradeOrderDetail(request | params)
        data = self.safe_value(response, 'data', None)
        if data is None:
            raise OrderNotFound(f'{self.id} fetchOrder() could not find order {params}')
        return self.parse_order(data, market)

    def get_trade_order_tpsl_detail(self, symbol: Str = None, params={}) -> Order:
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'instId': market['id'],
        }
        response = self.privateGetTradeOrderTpslDetail(request | params)
        data = self.safe_value(response, 'data', None)
        if data is None:
            raise OrderNotFound(f'{self.id} fetchOrder() could not find order {params}')
        return self.parse_order(data, market)

    def fetch_order(self, id: str, symbol: Str = None, params={}) -> Order:
        if params.get('stop'):
            params.pop('stop')
            client_order_id = params.pop('clientOrderId', None)
            if client_order_id is None:
                raise Exception(f'{self.id} fetchOrder() requires a clientOrderId param when fetching stop order')
            try:
                return self.get_trade_order_detail(symbol, params | {'algoClientOrderId': client_order_id})
            except OrderNotFound:
                algo_order = self.get_trade_order_tpsl_detail(symbol, params | {'clientOrderId': client_order_id})
                if algo_order['status'] == 'closed':
                    return self.get_trade_order_detail(symbol, params | {'algoClientOrderId': client_order_id})
                return algo_order
        else:
            return self.get_trade_order_detail(symbol, params)

    def fetch_markets(self, params={}) -> List[Market]:
        markets = super().fetch_markets(params)
        markets = [market for market in markets if market[self.options['defaultSubType']]]
        if self.options['defaultSubType'] == 'linear':
            markets = [market for market in markets if market['quote'] == 'USDT']
        return markets

    def cancel_order(self, id: str, symbol: Str = None, params={}):
        is_stop = params.pop('stop', None)
        if not is_stop:
            return super().cancel_order(id, symbol, params)
        client_order_id = params.get('clientOrderId')
        try:
            order = self.get_trade_order_detail(symbol, {'algoClientOrderId': client_order_id})
            return super().cancel_order(order['id'], symbol)
        except OrderNotFound:
            super().cancel_order(id, symbol, params | {'trigger': True})

    def parse_positions(self, positions, symbols: Optional[List[str]] = None, params={}):
        filtered_positions = [position for position in positions if position.get('instId') in self.markets_by_id]
        return super().parse_positions(filtered_positions, symbols, params)

    def parse_position(self, position: dict, market: Market = None):
        position = super().parse_position(position, market)
        position['is_long'] = position['side'] == 'long'
        position['liquidation_price'] = position['liquidationPrice']
        position['margin_type'] = position['marginMode']
        position['realizedPnl'] = None
        position['maintenance_margin'] = position['collateral']
        position['display_maintenance_margin'] = position['collateral']
        quantity_abs = self.get_quantity(position['contracts'], position['contractSize'])
        quantity = quantity_abs * (1 if position['is_long'] else -1)
        position['quantity'] = quantity
        if position['notional'] is None:
            notional = float(Precise.string_mul(str(quantity_abs), str(position['entryPrice'])))
            position['notional'] = notional
        return position

    def parse_order(self, order: dict, market: Market = None) -> Order:
        order = super().parse_order(order, market)
        market = market or self.market(order['symbol'])
        contractSize = market['contractSize']
        if order['amount'] is not None:
            order['amount'] = self.get_quantity(order['amount'], contractSize)
        if order['filled'] is not None:
            order['filled'] = self.get_quantity(order['filled'], contractSize)
        if order['remaining'] is not None:
            order['remaining'] = self.get_quantity(order['remaining'], contractSize)
        return order
