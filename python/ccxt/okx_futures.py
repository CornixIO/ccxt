from typing import Any

from base.types import Market, Order
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

    def _calculate_position_quantity(self, position: dict, contracts: float, contract_size: float):
        contracts_string = self.number_to_string(contracts)
        quantity_abs_string = contracts_abs_string = Precise.string_abs(contracts_string)
        if contract_size is not None:
            contract_size_string = self.number_to_string(contract_size)
            quantity_abs_string = Precise.string_mul(contracts_abs_string, contract_size_string)
        return self.parse_number(quantity_abs_string)
