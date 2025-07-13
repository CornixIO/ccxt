from typing import List
from ccxt.bingx_abs import bingx_abs
from ccxt.base.types import Market

BINGX_FUTURES = 'BingX Futures'


class bingx_futures(bingx_abs):
    def __init__(self, config={}):
        super().__init__(config)
        self.options['defaultType'] = 'swap'
        self.swapV2PrivateGetTradeOrder = self._swapV2PrivateGetTradeOrder

    def get_symbol_max_leverage(self, symbol: str) -> int | None:
        asset, pair = symbol.split('/')
        if pair in 'USDT':
            if asset in {'BTC', 'XRP'}:
                return 125
            elif asset in {'ETH', 'SOL'}:
                return 100
            elif asset in {'LINK', 'BCH', 'ADA', 'LTC', 'DOT', 'AVAX', 'SAND', 'ATOM', 'UNI', 'FIL', 'AAVE', 'DOGE',
                           'TRX', 'MASK', 'BNB', 'GALA', 'ETC', 'ROSE', 'API3', 'PEOPLE', 'KDA', 'APT', 'MAGIC', 'TRB',
                           'FLOKI', 'ID', 'TURBO', '1000PEPE', 'BIGTIME', 'CETUS', 'XAI', 'WIF', 'ZETA', 'BOME', 'TNSR',
                           'MEW', 'DOGS', 'MBOX', 'POL', 'NEIROETH', 'GHST', 'EIGEN', 'SAFE', 'KAIA', 'PNUT', 'AKT',
                           'ME', 'DEGO', 'VELODROME', 'PENGU', 'HYPE', 'HIVE', 'DF', 'AIXBT', 'VIRTUAL', 'CGPT',
                           'FARTCOIN', 'KMNO', 'GRIFFAIN', 'AI16Z', 'ZEREBRO', 'BIO', 'COOKIE', 'SONIC', 'D', 'S',
                           'VTHO', 'ANIME', 'BERA', 'KAITO', 'REDSTONE', 'FORM', 'NIL', 'PARTI', 'PAXG', 'GUN',
                           'KERNEL', 'WCT', 'HYPERLANE', 'SIGN', 'PUNDIX', 'ASR', 'ALPINE', 'SYRUP', 'B', 'HUMA', 'A',
                           'SOPH'}:
                return 75
            elif asset in {'THETA', 'ALGO', 'AXS', 'DYDX', 'SHIB', 'ICP', 'KSM', 'VET', 'SUSHI', 'NEAR', 'BSV', 'CHZ',
                           'SNX', 'CRV', 'LRC', 'YFI', 'MKR', 'GRT', 'ENS', 'BAT', 'STORJ', 'IMX', 'XLM', 'ONT', 'ONE',
                           'HBAR', 'KAVA', 'YGG', 'KNC', 'ZIL', 'FLOW', 'RUNE', 'RVN', 'IOST', 'MINA', 'AGLD', 'BAKE',
                           'WOO', 'LUNC', 'OP', 'LDO', 'INJ', 'ETHW', 'TONCOIN', 'FET', 'CORE', 'METIS', 'ASTR', 'STX',
                           'IOTA', 'TWT', 'EDU', 'SUI', 'BNT', 'KAS', 'POWR', 'TIA', 'CAKE', 'TOKEN', 'NTRN', 'PYTH',
                           'SUPER', 'ONG', 'JTO', 'MOVR', 'ONDO', 'LSK', 'JUP', 'OM', 'STRK', 'MYRO', 'VANRY', 'SLERF',
                           'ENA', 'REZ', 'BRETT', 'BLAST', 'SYN', 'SYS', 'CATI', 'POPCAT', 'SWELL', 'FLUX', 'NEIROCTO',
                           'RPL', '10000WHY', 'GOAT', 'GRASS', 'MOODENG', '1000000MOG', 'X', 'CHILLGUY', 'MORPHO',
                           'AERO', 'AVA', 'VANA', 'LUMIA', 'PHA', 'FUEL', 'ALCH', 'SWARMS', 'PROM', 'SOLV', 'MELANIA',
                           'VINE', 'IP', 'WAL', 'FUNTOKEN', 'MLN', 'XAUT', 'BABY', 'SOON', '1000000BOB'}:
                return 50
            elif asset in {'CELR', 'ENJ', 'SKL', 'ALPHA', 'CVC', 'JST', 'JASMY', 'ANKR', 'HOT', 'PERP', 'STG', 'SFP',
                           'GMX', 'HIGH', 'COTI', 'RLC', 'XCN', 'SXP', 'ARB', 'PENDLE', 'HIFI', 'POLYX', 'GAS', 'MEME',
                           'RATS', 'AUCTION', 'DYM', 'GLM', 'PORTAL', 'DOG', 'ATH', 'UXLINK', 'PRCL', 'RENDER', 'PONKE',
                           'RARE', 'G', 'VOXEL', 'SUNDOG', 'PUFFER', 'ZRC', 'OL', 'MOVE', 'ARC', 'AVAAI', 'J', 'PIPPIN',
                           'VVV', 'LAYER', 'B3', 'SHELL', 'GPS', 'PI', 'BMT', 'MUBARAK', 'KOMA', 'BANANAS31', 'BR',
                           'SIREN', 'BROCCOLIF3B', 'ORCA', 'PLUME', 'FIS', 'LA'}:
                return 25
            elif asset in {'MANA', 'ZRX', '1INCH', 'COMP', 'AR', 'EGLD', 'CELO', 'CHR', 'APE', 'RSR', 'GMT', 'NEO',
                           'CFX', 'SLP', 'MTL', 'LUNA', 'FLM', 'ICX', 'QNT', 'ARPA', 'HOOK', 'GTC', 'FXS', 'USTC',
                           'DUSK', 'BLUR', 'PHB', 'ACH', 'ILV', 'LPT', 'ATA', 'CKB', 'SUN', 'SSV', 'TLM', 'TRU', 'LQTY',
                           'JOE', 'ORDI', 'UMA', 'NMR', 'MAV', 'WLD', 'OXT', 'CYBER', 'SEI', 'SNT', 'BEAM', '1000BONK',
                           'CTC', 'ACE', 'NFP', 'MANTA', 'ALT', 'TAO', 'PIXEL', 'AEVO', 'ETHFI', 'DEGEN', 'W', 'SAGA',
                           'OMNINETWORK', 'MERL', 'BB', 'NOT', 'IO', '1000000BABYDOGE', 'ZK', 'LISTA', 'ZRO', 'BANANA',
                           'CLOUD', 'CHESS', 'QUICK', 'FIDA', 'FIO', 'LOKA', 'HMSTR', 'COS', 'DIA', 'DBR', '1000CAT',
                           'SCR', 'SANTOS', 'COW', 'DRIFT', 'HIPPO', 'RAY', 'THE', 'USUAL', 'ALTCOIN', 'RDNT',
                           'TRUMPSOL', 'TOSHI', 'FORTH', 'HEI', 'BROCCOLI', 'ROAM', 'SERAPH', 'VIC', 'ELX', 'EPIC',
                           'TUT', 'BID', 'RFC', 'PROMPT', 'PUMPBTC', 'FHE', 'STO', 'DARK', 'DEEP', 'INIT', 'BANK',
                           'EPT', 'ZORA', 'TAI', 'MILK', 'AIOT', 'HAEDAL', 'HOUSE', 'DOLO', 'GORK', 'B2', 'OBOL', 'SXT',
                           'DOOD', 'OG', 'ZKJ', 'SKYAI', 'RDAC', 'PRAI', 'NXPC', 'KILO', 'AGT', 'REX', 'AWE', 'BLUEFIN',
                           'ZBCN'}:
                return 20
            elif asset in {'1000CHEEMS'}:
                return 15
            elif asset in {'LAUNCHCOIN'}:
                return 13
            elif asset in {'CTK'}:
                return 11
            elif asset in {'BSW', '10000SATS', 'MAVIA', 'AERGO', 'ACT', 'TST', 'TROLLSOL', 'TGT', 'PFVS', 'RWA', 'ELDE',
                           'FLOCK', 'ASRR', 'BDXN', 'RDO', 'PORT3'}:
                return 10
            elif asset in {'ARK', 'BAN'}:
                return 8
            elif asset in {'XTER'}:
                return 5
        elif pair in 'USDC':
            if asset in {'BTC', 'ETH'}:
                return 125
            elif asset in {'SOL'}:
                return 100
            elif asset in {'DOGE', 'XRP', 'BNB', 'WLD', 'LTC', 'BCH', 'AVAX', 'FIL', 'DOT', 'XLM', 'ADA', 'HBAR', 'TRX',
                           'APT', 'ALGO', 'UNI', 'EIGEN', 'AAVE', 'PNUT', 'CATI', 'ME', 'GALA'}:
                return 75
            elif asset in {'1000PEPE', 'WIF', 'SUI', 'ARB', 'ENA', '1000BONK', 'NEAR', 'LINK', 'TIA', 'POPCAT', 'ONDO',
                           'NOT', 'OP', 'POL', 'ETC', 'STRK', 'SHIB'}:
                return 50
            elif asset in {'TONCOIN', 'AEVO', 'CRV', 'STX', 'ENS', 'VANA', 'IP', 'KAITO', 'BERA', 'FARTCOIN'}:
                return 25
            elif asset in {'ORDI', 'BOME', 'ETHFI', 'NEO'}:
                return 20
            elif asset in {'ACT'}:
                return 10
        return None

    def fetch_markets(self, params={}) -> List[Market]:
        return self.fetch_swap_markets(params)

    def parse_market(self, market: dict) -> Market:
        market_obj = super().parse_market(market)
        if market_obj is not None:
            symbol = market_obj['symbol']
            symbol = symbol.replace(':USDT', '').replace(':USDC', '')
            if '/USDC' in symbol:
                market_obj['active'] = False
            market_obj['symbol'] = symbol
            market_obj['limits']['leverage']['max'] = self.get_symbol_max_leverage(symbol)
        return market_obj

    def _swapV2PrivateGetTradeOrder(self, request):
        if 'clientOrderId' in request:
            request.pop('orderId', None)
        return super().swapV2PrivateGetTradeOrder(request)
