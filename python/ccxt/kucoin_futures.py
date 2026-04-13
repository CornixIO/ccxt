# -*- coding: utf-8 -*-

from ccxt.kucoinfutures import kucoinfutures
from ccxt.kucoin_abs import KucoinAbs
from ccxt.base.errors import InvalidOrder
from ccxt.base.precise import Precise

THIRTY_SECS_IN_MILLI = 1000 * 30


class kucoin_futures(KucoinAbs, kucoinfutures):
    def describe(self):
        return self.deep_extend(super().describe(), {
            'api': {
                'futuresPrivate': {
                    'get': {
                        'position/getPositionMode': 1,
                    },
                },
            },
            'options': {
                'versions': {
                    'futuresPrivate': {
                        'GET': {
                            'position/getPositionMode': 'v2',
                        },
                    },
                },
            },
        })

    def fetch_position_mode(self, symbol=None, params={}):
        response = self.futuresPrivateGetPositionGetPositionMode(params)
        data = self.safe_value(response, 'data', {})
        positionMode = self.safe_string(data, 'positionMode')
        hedged = positionMode == '1'
        return {'hedged': hedged, 'info': response}

    def fetch_markets(self, params={}):
        markets = super().fetch_markets(params)
        result = []
        for market in markets:
            if not market['linear'] or not market['swap']:
                continue
            settle = market['settle']
            market['symbol'] = market['symbol'].replace(':' + settle, '')
            contract_size = market['contractSize']
            market['precision']['amount'] *= contract_size
            market['limits']['amount']['min'] *= contract_size
            market['limits']['amount']['max'] *= contract_size
            result.append(market)
        return result

    def create_contract_order_request(self, symbol, type, side, amount, price=None, params={}):
        market = self.market(symbol)
        cs = self.safe_string(market, 'contractSize')
        adjusted = self.parse_number(Precise.string_div(self.amount_to_precision(symbol, amount), cs))
        return super().create_contract_order_request(symbol, type, side, adjusted, price, params)

    def change_auto_deposit(self, symbol, is_auto_deposit):
        assert is_auto_deposit is not None
        self.load_markets()
        _id = self.market_id(symbol)
        response = self.futuresPrivatePostPositionMarginAutoDepositStatus({'symbol': _id, 'status': is_auto_deposit})
        return response['data']

    def change_margin_type(self, symbol, is_cross):
        assert is_cross is not None
        self.load_markets()
        _id = self.market_id(symbol)
        margin_mode_str = 'CROSS' if is_cross else 'ISOLATED'
        response = self.futuresPrivatePostPositionChangeMarginMode({'symbol': _id, 'marginMode': margin_mode_str})
        return response['data']['marginMode'] == 'CROSS'

    def set_leverage(self, symbol, leverage, params={}):
        self.load_markets()
        _id = self.market_id(symbol)
        return self.futuresPrivatePostChangeCrossUserLeverage({'symbol': _id, 'leverage': leverage})

    def fetch_positions(self, symbol=None, params={}):
        self.load_markets()
        if symbol:
            response = self.futuresPrivateGetPosition({'symbol': self.market_id(symbol)})
            positions = [self.safe_value(response, 'data')]
        else:
            response = self.futuresPrivateGetPositions(params)
            positions = self.safe_value(response, 'data', [])
        return [
            self.parse_position(p)
            for p in positions
            if self.safe_string(p, 'symbol') in self.markets_by_id
        ]

    def parse_position(self, position, market=None):
        result = super().parse_position(position, market)
        mkt = self.safe_market(self.safe_string(position, 'symbol'), market)
        cs = self.safe_value(mkt, 'contractSize', 1)
        qty = self.safe_float(position, 'currentQty', 0)
        result['quantity'] = qty * cs
        result['contract_size'] = cs
        crossMode = self.safe_value(position, 'crossMode')
        auto_deposit = self.safe_value(position, 'autoDeposit')
        result['margin_type'] = 'cross' if crossMode or auto_deposit else 'isolated'
        return result

    def parse_order(self, order, market=None):
        result = super().parse_order(order, market)
        market_id = self.safe_string(order, 'symbol') if order else None
        mkt = self.safe_market(market_id, market)
        cs = self.safe_string(mkt, 'contractSize') if mkt else None
        if cs:
            for key in ('amount', 'filled', 'remaining'):
                value = result.get(key)
                if value is not None:
                    result[key] = self.parse_number(Precise.string_mul(str(value), cs))
        return result

    def get_positions(self, symbol=None, params=None):
        return self.fetch_positions(symbol, params or {})

    def fetch_stop_order_from_orders(self, responseData, id, symbol):
        is_active = responseData.get('isActive')
        stop_price_type = responseData.get('stopPriceType')
        if is_active or not stop_price_type:
            return None
        relevant_time = self.safe_float(responseData, 'updatedAt') or self.safe_float(responseData, 'endAt') or self.safe_float(responseData, 'createdAt')
        if not relevant_time:
            return None
        since = int(relevant_time) - THIRTY_SECS_IN_MILLI
        orders = self.fetch_closed_orders(symbol, since=since)
        order = next((o for o in orders if o['id'] == id), None)
        if not order:
            orders = self.fetch_open_orders(symbol, since=since)
            order = next((o for o in orders if o['id'] == id), None)
        return order

    def fetch_order(self, id=None, symbol=None, params={}):
        self.load_markets()
        request = {}
        method = 'futuresPrivateGetOrdersOrderId'
        if id is None:
            clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
            if clientOrderId is None:
                raise InvalidOrder(self.id + ' fetchOrder() requires parameter id or params.clientOid')
            request['clientOid'] = clientOrderId
            method = 'futuresPrivateGetOrdersByClientOid'
            params = self.omit(params, ['clientOid', 'clientOrderId'])
        else:
            request['orderId'] = id
        response = getattr(self, method)(self.extend(request, params))
        market = self.market(symbol) if symbol is not None else None
        responseData = self.safe_value(response, 'data')
        stop_parsed_order = self.fetch_stop_order_from_orders(responseData, id, symbol)
        if stop_parsed_order:
            return stop_parsed_order
        return self.parse_order(responseData, market)


if __name__ == '__main__':
    from pprint import pprint
    k = kucoin_futures()
    pprint(k.load_markets()['BTC/USDT'])