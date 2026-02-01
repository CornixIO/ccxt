from typing import Any

from ccxt.base.precise import Precise
from ccxt.base.types import Market, Order
from ccxt.okx_abs import okx_abs

OKX_FUTURES = 'OKX Futures'


class okx_futures(okx_abs):
    def should_filter_balance_asset(self, code: str) -> bool:
        return code != 'USDT'

    def describe(self) -> Any:
        return self.deep_extend(super(okx_futures, self).describe(), {
            'options': {
                'defaultType': 'linear',
            },
        })

    def parse_market(self, market: dict) -> Market:
        parsed_market = super().parse_market(market)
        if parsed_market is not None:
            contract_size = self.safe_string(parsed_market, 'contractSize')
            if contract_size is not None:
                amount_precision = self.safe_string(parsed_market['precision'], 'amount')
                min_amount = self.safe_string(parsed_market['limits']['amount'], 'min')
                if amount_precision is not None:
                    amount_precision = Precise.string_mul(amount_precision, contract_size)
                    parsed_market['precision']['amount'] = self.parse_number(amount_precision)
                if min_amount is not None:
                    min_amount = Precise.string_mul(min_amount, contract_size)
                    parsed_market['limits']['amount']['min'] = self.parse_number(min_amount)
        return parsed_market

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        size = self.amount_to_precision(symbol, amount)
        contract_size = self.safe_value(market, 'contractSize')
        if contract_size is not None:
            size = Precise.string_div(size, str(contract_size))
            size = float(size)
        params['sz'] = size
        return super().create_order(symbol, type, side, amount, price, params)

    def parse_order(self, order: dict, market: Market = None) -> Order:
        parsed_order = super().parse_order(order, market)
        if parsed_order is not None and market is None:
            symbol = self.safe_string(parsed_order, 'symbol')
            if symbol is not None:
                market = self.safe_market(symbol)
        contract_size = self.safe_value(market, 'contractSize')
        if contract_size is not None:
            amount = self.safe_string(parsed_order, 'amount')
            if amount is not None:
                contract_size_string = self.number_to_string(contract_size)
                amount = Precise.string_mul(amount, contract_size_string)
                parsed_order['amount'] = self.parse_number(amount)
            filled = self.safe_string(parsed_order, 'filled')
            if filled is not None:
                contract_size_string = self.number_to_string(contract_size)
                filled = Precise.string_mul(filled, contract_size_string)
                parsed_order['filled'] = self.parse_number(filled)
        return parsed_order

    def _calculate_position_quantity(self, position: dict, contracts: float, contract_size: float):
        contracts_string = self.number_to_string(contracts)
        quantity_abs_string = contracts_abs_string = Precise.string_abs(contracts_string)
        if contract_size is not None:
            contract_size_string = self.number_to_string(contract_size)
            quantity_abs_string = Precise.string_mul(contracts_abs_string, contract_size_string)
        return self.parse_number(quantity_abs_string)
