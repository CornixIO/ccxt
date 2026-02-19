from base.types import Account
from ccxt import OrderNotFound
from ccxt.base.precise import Precise
from ccxt.base.types import Balances, Market, Str, Order, Int
from ccxt.okx import okx

TO_FLOAT_PARAMS = {'sz', 'slOrdPx', 'slTriggerPx', 'tpOrdPx', 'tpTriggerPx', 'orderPx', 'triggerPx', 'px'}
PERMISSION_TO_VALUE = {"spot": ["read_only", "trade"], "futures": ["read_only", "trade"]}
ACCOUNT_MODES = {"margin_free": 1, "single_currency_margin": 2, "multi_currency_margin": 3, "portfolio_margin": 4}



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
            tick_size = self.safe_string(market, 'tickSz')
            precision_price = self.parse_number(tick_size)
            parsed_market['limits']['price'] = {'min': precision_price, 'max': None}
        return parsed_market

    def parse_markets(self, markets):
        parsed_markets = super().parse_markets(markets)
        relevant_markets = []
        for parsed_market in parsed_markets:
            if parsed_market[self.options['defaultType']] is True:
                relevant_markets.append(parsed_market)
        return relevant_markets

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

    def fetch_order(self, id: str, symbol: Str = None, params={}) -> Order:
        try:
            return super().fetch_order(id, symbol, params=params)
        except OrderNotFound:
            if params.pop('stop', None):
                # BACKWARDS
                result = super().fetch_order(id, symbol, params=params)
                result['id'] = result['info']['ordId']
                return result
            raise

    def fetch_order_trades(self, id: str, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        if params.get('stop'):
            order = self.fetch_order(id, symbol, params.copy())
            params.pop('stop')
            return super().fetch_order_trades(order['info']['ordId'], symbol, since, limit, params)
        else:
            return super().fetch_order_trades(id, symbol, since, limit, params)

    def get_parsed_account(self, account):
        accountId = self.safe_string(account, 'uid')
        mainUid = self.safe_string(account, 'mainUid')
        account_mode = self.safe_integer(account, 'acctLv')
        margin_free = account_mode == ACCOUNT_MODES.get("margin_free")
        multi_currency_margin = account_mode == ACCOUNT_MODES.get("multi_currency_margin")
        portfolio_margin = account_mode == ACCOUNT_MODES.get("portfolio_margin")
        position_mode = self.safe_string(account, 'posMode')
        role_type = self.safe_integer(account, 'roleType')
        spot_role_type = self.safe_integer(account, 'spotRoleType')
        ips = self.safe_string(account, 'ip')
        exchange_permissions = self.safe_string(account, 'perm').split(',')
        read_only = 'trade' not in exchange_permissions
        permissions = self.extract_trading_permissions(PERMISSION_TO_VALUE, permissions_list=exchange_permissions)
        return {
            'uid': accountId,
            'main_uid': mainUid,
            'margin_free': margin_free,
            'multi_currency_margin': multi_currency_margin,
            'portfolio_margin': portfolio_margin,
            'position_mode': position_mode,
            'role_type': role_type,
            'spot_role_type': spot_role_type,
            'ips': ips,
            'permissions': permissions,
            'read_only': read_only,
            'ip_restrict': bool(ips),
            'info': account,
        }

    def get_api_account_details(self):
        accounts = self.fetch_accounts()
        for account in accounts:
            account_info = account['info']
            if account_info["uid"] == account_info["mainUid"]:
                return self.get_parsed_account(account_info)
        return self.get_parsed_account(accounts[0]['info'])