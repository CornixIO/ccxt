from ccxt.binance import binance
from ccxt.base.types import Market

PERMISSION_TO_VALUE = {"spot": ["enableSpotAndMarginTrading"], "futures": ["enableFutures"],
                       "withdrawal": ["enableWithdrawals"]}


class binance_abs(binance):
    def is_inverse(self, *args, **kwargs):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'delivery'

    def is_linear(self, *args, **kwargs):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'future'

    def get_api_account_details(self):
        response = self.sapi_get_account_apirestrictions()
        permissions = self.extract_trading_permissions(PERMISSION_TO_VALUE, response=response)
        return {
            'info': response,
            "creation": self.safe_integer(response, "createTime"),
            "expiration": self.safe_integer(response, "tradingAuthorityExpirationTime"),
            "permissions": permissions,
            "ip_restrict": self.safe_value(response, "ipRestrict")
        }

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            symbol = market_obj['symbol'].split(':')[0]
            market_obj['symbol'] = symbol
        return market_obj
