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

    def _calculate_position_quantity(self, position: dict, contracts: float, contract_size: float):
        contracts_string = self.number_to_string(contracts)
        quantity_abs_string = contracts_abs_string = Precise.string_abs(contracts_string)
        if contract_size is not None:
            contract_size_string = self.number_to_string(contract_size)
            quantity_abs_string = Precise.string_mul(contracts_abs_string, contract_size_string)
        return self.parse_number(quantity_abs_string)

    def _apply_contract_size_to_order(self, order, contract_size):
        if order.get('amount') is not None:
            order['amount'] = self.parse_number(Precise.string_mul(str(order['amount']), str(contract_size)))
        if order.get('filled') is not None:
            order['filled'] = self.parse_number(Precise.string_mul(str(order['filled']), str(contract_size)))
        if order.get('remaining') is not None:
            order['remaining'] = self.parse_number(Precise.string_mul(str(order['remaining']), str(contract_size)))
        return order

    def parse_order(self, order: dict, market: Market = None) -> Order:
        order = super().parse_order(order, market)
        if market is None and order.get('symbol'):
            try:
                market = self.market(order['symbol'])
            except Exception:
                market = None
        if market is not None:
            contract_size = market.get('contractSize')
            if contract_size is not None:
                order = self._apply_contract_size_to_order(order, contract_size)
        return order
