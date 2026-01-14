from typing import Any

from ccxt import PermissionDenied
from ccxt.bitget import bitget


class bitget_abs(bitget):
    def __init__(self, config={}):
        super().__init__(config)
        self.headers['locale'] = 'en-US'
        self.has['fetchCurrencies'] = False

    def describe(self) -> Any:
        return self.deep_extend(super().describe(), {
            'exceptions': {
                'exact': {
                    '40013': PermissionDenied,  # {"code":"40013","msg":"User status is abnormal","requestTime":1768398859928,"data":null}
                }
            }
        })
