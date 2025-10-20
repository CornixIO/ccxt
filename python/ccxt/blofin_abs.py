from typing import Any, List

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

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            info = market_obj['info']
            market_obj['symbol'] = market_obj['symbol'].split(':')[0]
            contract_size_str = str(market_obj['contractSize'])
            limits = market_obj['limits']
            limits['amount']['max'] = float(Precise.string_mul(info['maxLimitSize'], contract_size_str))
            limits['markets'] = {'min': 0., 'max': float(Precise.string_mul(info['maxMarketSize'], contract_size_str))}
            market_obj['precision']['amount'] = float(Precise.string_mul(str(market_obj['precision']['amount']), str(contract_size_str)))
            contract_type = info['contractType']
            market_obj['linear'] = contract_type == 'linear'
            market_obj['inverse'] = contract_type == 'inverse'
        return market_obj

    def fetch_order_by_algo_client_order_id(self, symbol: Str = None, client_order_id: Str = None, params={}) -> Order:
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'instId': market['id'],
            'algoClientOrderId': client_order_id,
        }
        response = self.privateGetTradeOrderDetail(request | params)
        data = self.safe_value(response, 'data', None)
        if data is None:
            raise OrderNotFound(f'{self.id} fetchOrder() could not find order {client_order_id}')
        return self.parse_order(data, market)

    def fetch_order(self, id: str, symbol: Str = None, params={}) -> Order:
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'instId': market['id'],
        }
        fetch_search_order = []
        clientOrderId = self.safe_string(params, 'clientOrderId')
        if clientOrderId is None:
            raise Exception(f'{self.id} fetchOrder() requires a clientOrderId param')
        is_stop = params.pop('type', '') == 'stop'
        if is_stop:
            fetch_search_order.append([self.privateGetTradeOrderDetail, {'algoClientOrderId': clientOrderId}])
            fetch_search_order.append([self.privateGetTradeOrderTpslDetail, {'clientOrderId': clientOrderId}])
        else:
            fetch_search_order.append([self.privateGetTradeOrderDetail, {'clientOrderId': clientOrderId}])
        for fetch, request_params in fetch_search_order:
            response = fetch(request | request_params)
            data = self.safe_value(response, 'data', None)
            if data is not None:
                break
        else:
            raise OrderNotFound(f'{self.id} fetchOrder() could not find order {id}')
        return self.parse_order(data, market)

    def fetch_markets(self, params={}) -> List[Market]:
        markets = super().fetch_markets(params)
        markets = [market for market in markets if market[self.options['defaultSubType']]]
        if self.options['defaultSubType'] == 'linear':
            markets = [market for market in markets if market['quote'] == 'USDT']
        return markets

    def cancel_order(self, id: str, symbol: Str = None, params={}):
        order_type = params.pop('type', None)
        if order_type is None:
            return super().cancel_order(id, symbol, params)
        client_order_id = params.get('clientOrderId')
        try:
            order = self.fetch_order_by_algo_client_order_id(symbol, client_order_id)
            return super().cancel_order(order['id'], symbol)
        except OrderNotFound:
            super().cancel_order(id, symbol, params | {'trigger': True})

    def parse_position(self, position: dict, market: Market = None):
        position = super().parse_position(position, market)
        position['is_long'] = position['side'] == 'long'
        position['liquidation_price'] = position['liquidationPrice']
        position['margin_type'] = position['marginMode']
        position['realizedPnl'] = None
        position['maintenance_margin'] = position['collateral']
        position['display_maintenance_margin'] = position['collateral']
        quantity_abs = float(Precise.string_mul(str(position['contracts']), str(position['contractSize'])))
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
            order['amount'] = float(Precise.string_mul(str(order['amount']), str(contractSize)))
        if order['filled'] is not None:
            order['filled'] = float(Precise.string_mul(str(order['filled']), str(contractSize)))
        if order['remaining'] is not None:
            order['remaining'] = float(Precise.string_mul(str(order['remaining']), str(contractSize)))
        return order