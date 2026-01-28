from typing import Any

from ccxt.okx_abs import okx_abs

OKX = 'OKX'


class okx_spot(okx_abs):
    def describe(self) -> Any:
        return self.deep_extend(super(okx_spot, self).describe(), {
            'options': {
                'defaultType': 'spot',
            },
        })
