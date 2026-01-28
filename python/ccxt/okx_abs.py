from ccxt.base.precise import Precise
from ccxt.base.types import Balances, Market
from ccxt.okx import okx


class okx_abs(okx):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['brokerId'] = 'b5fa360738a048BC'

    def should_filter_balance_asset(self, code: str) -> bool:
        return False

    def fetch_balance(self, params={}) -> Balances:
        balance = super().fetch_balance(params)
        filtered_balance = {'info': balance['info']}
        for code in balance:
            if code in ['info', 'free', 'used', 'total', 'timestamp', 'datetime']:
                filtered_balance[code] = balance[code]
                continue
            if self.should_filter_balance_asset(code):
                continue
            filtered_balance[code] = balance[code]
        return self.safe_balance(filtered_balance)

    def parse_market(self, market: dict) -> Market:
        parsed_market = super().parse_market(market)
        if parsed_market is not None:
            symbol = parsed_market['symbol'].split(':')[0]
            parsed_market['symbol'] = symbol
            parsed_market['limits']['orders'] = {'max': 60}
            parsed_market['limits']['conditional_orders'] = {'max': 20}
        return parsed_market

    def _calculate_position_quantity(self, position: dict, contracts: float, contract_size: float):
        contracts_string = self.number_to_string(contracts)
        quantity_abs_string = Precise.string_abs(contracts_string)
        return self.parse_number(quantity_abs_string)

    def _apply_quantity_sign(self, quantity_abs: float, side: str, is_long: bool):
        if is_long is not None:
            side_factor = 1 if is_long else -1
        else:
            side_factor = 1 if side == 'long' else -1
        quantity_abs_string = self.number_to_string(quantity_abs)
        side_factor_string = self.number_to_string(side_factor)
        quantity_string = Precise.string_mul(quantity_abs_string, side_factor_string)
        return self.parse_number(quantity_string)

    def parse_position(self, position: dict, market: Market = None):
        position = super().parse_position(position, market)
        side = self.safe_string(position, 'side')
        hedged = self.safe_value(position, 'hedged', False)
        is_long = side == 'long' if hedged else None
        position['is_long'] = is_long
        position['margin_type'] = self.safe_string(position, 'marginMode')
        position['liquidation_price'] = self.safe_value(position, 'liquidationPrice')
        if self.safe_value(position, 'realizedPnl') is None:
            position['realizedPnl'] = None
        position['maintenance_margin'] = self.safe_value(position, 'collateral')
        position['display_maintenance_margin'] = self.safe_value(position, 'collateral')
        contracts = self.safe_value(position, 'contracts')
        contract_size = self.safe_value(position, 'contractSize')
        quantity_abs = self._calculate_position_quantity(position, contracts, contract_size)
        quantity = self._apply_quantity_sign(quantity_abs, side, is_long)
        position['quantity'] = quantity
        if self.safe_value(position, 'notional') is None and self.safe_value(position, 'entryPrice') is not None:
            entry_price_string = self.number_to_string(self.safe_value(position, 'entryPrice'))
            quantity_abs_string = self.number_to_string(quantity_abs)
            notional_string = Precise.string_mul(quantity_abs_string, entry_price_string)
            position['notional'] = self.parse_number(notional_string)
        return position
