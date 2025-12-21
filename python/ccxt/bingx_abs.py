from typing import Any
from ccxt.base.errors import PermissionDenied, OrderNotFound, OperationFailed, InsufficientFunds, BadRequest, \
    ExchangeError
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
                    '80012': ExchangeError,
                    '100004': PermissionDenied,
                    '100413': PermissionDenied,
                    '101253': InsufficientFunds,  # {"code":101253,"msg":"Insufficient margin","data":{}}
                    '109400': BadRequest,
                    '109421': OrderNotFound,
                    '109422': OrderNotFound,
                    '109429': OperationFailed,
                    '112415': PermissionDenied,  # {"code":112415,"msg":"Transaction failed. As per compliance requirements, your account needs to complete advanced verification.","data":{}}
                }
            }
        })

    def is_inverse(self):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'inverse'

    def is_linear(self):
        default_type = self.safe_string(self.options, 'defaultType')
        return default_type == 'future'
