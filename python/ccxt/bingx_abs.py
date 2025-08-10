from typing import Any
from ccxt.base.errors import PermissionDenied
from ccxt.bingx import bingx


class bingx_abs(bingx):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['broker'] = 'Cornix'

    def describe(self) -> Any:
        return self.deep_extend(super().describe(), {
            'commonCurrencies': {
                'TONCOIN': 'TON',
            },
            'exceptions': {
                'exact': {
                    '100413': PermissionDenied,
                }
            }
        })

    def is_inverse(self):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'inverse'

    def is_linear(self):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'future'
