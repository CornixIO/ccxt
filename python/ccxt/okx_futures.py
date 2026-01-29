from typing import Any

from ccxt.base.precise import Precise
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

    def _calculate_position_quantity(self, position: dict, contracts: float, contract_size: float):
        contracts_string = self.number_to_string(contracts)
        quantity_abs_string = contracts_abs_string = Precise.string_abs(contracts_string)
        if contract_size is not None:
            contract_size_string = self.number_to_string(contract_size)
            quantity_abs_string = Precise.string_mul(contracts_abs_string, contract_size_string)
        return self.parse_number(quantity_abs_string)
