# -*- coding: utf-8 -*-

"""CCXT: CryptoCurrency eXchange Trading Library (Async)"""

# -----------------------------------------------------------------------------

__version__ = '4.0.106.95'

# -----------------------------------------------------------------------------

from ccxt.async_support.base.exchange import Exchange                   # noqa: F401

from ccxt.base.decimal_to_precision import decimal_to_precision  # noqa: F401
from ccxt.base.decimal_to_precision import TRUNCATE              # noqa: F401
from ccxt.base.decimal_to_precision import ROUND                 # noqa: F401
from ccxt.base.decimal_to_precision import DECIMAL_PLACES        # noqa: F401
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS    # noqa: F401
from ccxt.base.decimal_to_precision import NO_PADDING            # noqa: F401
from ccxt.base.decimal_to_precision import PAD_WITH_ZERO         # noqa: F401

from ccxt.base import errors                                # noqa: F401
from ccxt.base.errors import BaseError                      # noqa: F401
from ccxt.base.errors import ExchangeError                  # noqa: F401
from ccxt.base.errors import AuthenticationError            # noqa: F401
from ccxt.base.errors import PermissionDenied               # noqa: F401
from ccxt.base.errors import AccountSuspended               # noqa: F401
from ccxt.base.errors import AccountNotVerified             # noqa: F401
from ccxt.base.errors import ArgumentsRequired              # noqa: F401
from ccxt.base.errors import BadRequest                     # noqa: F401
from ccxt.base.errors import BadSymbol                      # noqa: F401
from ccxt.base.errors import BadResponse                    # noqa: F401
from ccxt.base.errors import NullResponse                   # noqa: F401
from ccxt.base.errors import InsufficientFunds              # noqa: F401
from ccxt.base.errors import InvalidAddress                 # noqa: F401
from ccxt.base.errors import AddressPending                 # noqa: F401
from ccxt.base.errors import InvalidOrder                   # noqa: F401
from ccxt.base.errors import OrderNotFound                  # noqa: F401
from ccxt.base.errors import TradesNotFound                 # noqa: F401
from ccxt.base.errors import OrderNotCached                 # noqa: F401
from ccxt.base.errors import CancelPending                  # noqa: F401
from ccxt.base.errors import OrderImmediatelyFillable       # noqa: F401
from ccxt.base.errors import OrderNotFillable               # noqa: F401
from ccxt.base.errors import DuplicateOrderId               # noqa: F401
from ccxt.base.errors import NotSupported                   # noqa: F401
from ccxt.base.errors import NetworkError                   # noqa: F401
from ccxt.base.errors import DDoSProtection                 # noqa: F401
from ccxt.base.errors import RateLimitExceeded              # noqa: F401
from ccxt.base.errors import AccountRateLimitExceeded       # noqa: F401
from ccxt.base.errors import ExchangeNotAvailable           # noqa: F401
from ccxt.base.errors import OnMaintenance                  # noqa: F401
from ccxt.base.errors import InvalidNonce                   # noqa: F401
from ccxt.base.errors import RequestTimeout                 # noqa: F401
from ccxt.base.errors import error_hierarchy                # noqa: F401


from ccxt.async_support.acx import acx                                    # noqa: F401
from ccxt.async_support.aofex import aofex                                # noqa: F401
from ccxt.async_support.bcex import bcex                                  # noqa: F401
from ccxt.async_support.bequant import bequant                            # noqa: F401
from ccxt.async_support.bibox import bibox                                # noqa: F401
from ccxt.async_support.bigone import bigone                              # noqa: F401
from ccxt.async_support.binance import binance                            # noqa: F401
from ccxt.async_support.binanceje import binanceje                        # noqa: F401
from ccxt.async_support.binanceus import binanceus                        # noqa: F401
from ccxt.async_support.bit2c import bit2c                                # noqa: F401
from ccxt.async_support.bitbank import bitbank                            # noqa: F401
from ccxt.async_support.bitbay import bitbay                              # noqa: F401
from ccxt.async_support.bitfinex import bitfinex                          # noqa: F401
from ccxt.async_support.bitfinex2 import bitfinex2                        # noqa: F401
from ccxt.async_support.bitflyer import bitflyer                          # noqa: F401
from ccxt.async_support.bitforex import bitforex                          # noqa: F401
from ccxt.async_support.bitget import bitget                              # noqa: F401
from ccxt.async_support.bithumb import bithumb                            # noqa: F401
from ccxt.async_support.bitkk import bitkk                                # noqa: F401
from ccxt.async_support.bitmart import bitmart                            # noqa: F401
from ccxt.async_support.bitmax import bitmax                              # noqa: F401
from ccxt.async_support.bitmex import bitmex                              # noqa: F401
from ccxt.async_support.bitpanda import bitpanda                          # noqa: F401
from ccxt.async_support.bitso import bitso                                # noqa: F401
from ccxt.async_support.bitstamp import bitstamp                          # noqa: F401
from ccxt.async_support.bitstamp1 import bitstamp1                        # noqa: F401
from ccxt.async_support.bittrex import bittrex                            # noqa: F401
from ccxt.async_support.bitvavo import bitvavo                            # noqa: F401
from ccxt.async_support.bitz import bitz                                  # noqa: F401
from ccxt.async_support.bl3p import bl3p                                  # noqa: F401
from ccxt.async_support.bleutrade import bleutrade                        # noqa: F401
from ccxt.async_support.braziliex import braziliex                        # noqa: F401
from ccxt.async_support.btcalpha import btcalpha                          # noqa: F401
from ccxt.async_support.btcbox import btcbox                              # noqa: F401
from ccxt.async_support.btcmarkets import btcmarkets                      # noqa: F401
from ccxt.async_support.btctradeua import btctradeua                      # noqa: F401
from ccxt.async_support.btcturk import btcturk                            # noqa: F401
from ccxt.async_support.buda import buda                                  # noqa: F401
from ccxt.async_support.bw import bw                                      # noqa: F401
from ccxt.async_support.bybit import bybit                                # noqa: F401
from ccxt.async_support.bytetrade import bytetrade                        # noqa: F401
from ccxt.async_support.cex import cex                                    # noqa: F401
from ccxt.async_support.chilebit import chilebit                          # noqa: F401
from ccxt.async_support.coinbase import coinbase                          # noqa: F401
from ccxt.async_support.coinbaseprime import coinbaseprime                # noqa: F401
from ccxt.async_support.coinbasepro import coinbasepro                    # noqa: F401
from ccxt.async_support.coincheck import coincheck                        # noqa: F401
from ccxt.async_support.coinegg import coinegg                            # noqa: F401
from ccxt.async_support.coinex import coinex                              # noqa: F401
from ccxt.async_support.coinfalcon import coinfalcon                      # noqa: F401
from ccxt.async_support.coinfloor import coinfloor                        # noqa: F401
from ccxt.async_support.coingi import coingi                              # noqa: F401
from ccxt.async_support.coinmarketcap import coinmarketcap                # noqa: F401
from ccxt.async_support.coinmate import coinmate                          # noqa: F401
from ccxt.async_support.coinone import coinone                            # noqa: F401
from ccxt.async_support.coinspot import coinspot                          # noqa: F401
from ccxt.async_support.coss import coss                                  # noqa: F401
from ccxt.async_support.crex24 import crex24                              # noqa: F401
from ccxt.async_support.currencycom import currencycom                    # noqa: F401
from ccxt.async_support.deribit import deribit                            # noqa: F401
from ccxt.async_support.digifinex import digifinex                        # noqa: F401
from ccxt.async_support.dsx import dsx                                    # noqa: F401
from ccxt.async_support.eterbase import eterbase                          # noqa: F401
from ccxt.async_support.exmo import exmo                                  # noqa: F401
from ccxt.async_support.exx import exx                                    # noqa: F401
from ccxt.async_support.fcoin import fcoin                                # noqa: F401
from ccxt.async_support.fcoinjp import fcoinjp                            # noqa: F401
from ccxt.async_support.flowbtc import flowbtc                            # noqa: F401
from ccxt.async_support.foxbit import foxbit                              # noqa: F401
from ccxt.async_support.ftx import ftx                                    # noqa: F401
from ccxt.async_support.gateio import gateio                              # noqa: F401
from ccxt.async_support.gemini import gemini                              # noqa: F401
from ccxt.async_support.hbtc import hbtc                                  # noqa: F401
from ccxt.async_support.hitbtc import hitbtc                              # noqa: F401
from ccxt.async_support.hollaex import hollaex                            # noqa: F401
from ccxt.async_support.huobijp import huobijp                            # noqa: F401
from ccxt.async_support.huobipro import huobipro                          # noqa: F401
from ccxt.async_support.huobiru import huobiru                            # noqa: F401
from ccxt.async_support.hyperliquid import hyperliquid                    # noqa: F401
from ccxt.async_support.hyperliquid_abs import hyperliquid_abs            # noqa: F401
from ccxt.async_support.hyperliquid_futures import hyperliquid_futures    # noqa: F401
from ccxt.async_support.hyperliquid_spot import hyperliquid_spot          # noqa: F401
from ccxt.async_support.ice3x import ice3x                                # noqa: F401
from ccxt.async_support.idex import idex                                  # noqa: F401
from ccxt.async_support.independentreserve import independentreserve      # noqa: F401
from ccxt.async_support.indodax import indodax                            # noqa: F401
from ccxt.async_support.itbit import itbit                                # noqa: F401
from ccxt.async_support.kraken import kraken                              # noqa: F401
from ccxt.async_support.kucoin import kucoin                              # noqa: F401
from ccxt.async_support.kucoinfutures import kucoinfutures                # noqa: F401
from ccxt.async_support.kuna import kuna                                  # noqa: F401
from ccxt.async_support.lakebtc import lakebtc                            # noqa: F401
from ccxt.async_support.latoken import latoken                            # noqa: F401
from ccxt.async_support.lbank import lbank                                # noqa: F401
from ccxt.async_support.liquid import liquid                              # noqa: F401
from ccxt.async_support.livecoin import livecoin                          # noqa: F401
from ccxt.async_support.luno import luno                                  # noqa: F401
from ccxt.async_support.lykke import lykke                                # noqa: F401
from ccxt.async_support.mercado import mercado                            # noqa: F401
from ccxt.async_support.mixcoins import mixcoins                          # noqa: F401
from ccxt.async_support.oceanex import oceanex                            # noqa: F401
from ccxt.async_support.okcoin import okcoin                              # noqa: F401
from ccxt.async_support.okx import okx                                  # noqa: F401
from ccxt.async_support.paymium import paymium                            # noqa: F401
from ccxt.async_support.phemex import phemex                              # noqa: F401
from ccxt.async_support.poloniex import poloniex                          # noqa: F401
from ccxt.async_support.probit import probit                              # noqa: F401
from ccxt.async_support.qtrade import qtrade                              # noqa: F401
from ccxt.async_support.rightbtc import rightbtc                          # noqa: F401
from ccxt.async_support.southxchange import southxchange                  # noqa: F401
from ccxt.async_support.stex import stex                                  # noqa: F401
from ccxt.async_support.stronghold import stronghold                      # noqa: F401
from ccxt.async_support.surbitcoin import surbitcoin                      # noqa: F401
from ccxt.async_support.therock import therock                            # noqa: F401
from ccxt.async_support.tidebit import tidebit                            # noqa: F401
from ccxt.async_support.tidex import tidex                                # noqa: F401
from ccxt.async_support.timex import timex                                # noqa: F401
from ccxt.async_support.upbit import upbit                                # noqa: F401
from ccxt.async_support.vaultoro import vaultoro                          # noqa: F401
from ccxt.async_support.vbtc import vbtc                                  # noqa: F401
from ccxt.async_support.wavesexchange import wavesexchange                # noqa: F401
from ccxt.async_support.whitebit import whitebit                          # noqa: F401
from ccxt.async_support.xbtce import xbtce                                # noqa: F401
from ccxt.async_support.xena import xena                                  # noqa: F401
from ccxt.async_support.yobit import yobit                                # noqa: F401
from ccxt.async_support.zaif import zaif                                  # noqa: F401
from ccxt.async_support.zb import zb                                      # noqa: F401

exchanges = [
    'acx',
    'aofex',
    'bcex',
    'bequant',
    'bibox',
    'bigone',
    'binance',
    'binanceje',
    'binanceus',
    'bit2c',
    'bitbank',
    'bitbay',
    'bitfinex',
    'bitfinex2',
    'bitflyer',
    'bitforex',
    'bitget',
    'bithumb',
    'bitkk',
    'bitmart',
    'bitmax',
    'bitmex',
    'bitpanda',
    'bitso',
    'bitstamp',
    'bitstamp1',
    'bittrex',
    'bitvavo',
    'bitz',
    'bl3p',
    'bleutrade',
    'braziliex',
    'btcalpha',
    'btcbox',
    'btcmarkets',
    'btctradeua',
    'btcturk',
    'buda',
    'bw',
    'bybit',
    'bytetrade',
    'cex',
    'chilebit',
    'coinbase',
    'coinbaseprime',
    'coinbasepro',
    'coincheck',
    'coinegg',
    'coinex',
    'coinfalcon',
    'coinfloor',
    'coingi',
    'coinmarketcap',
    'coinmate',
    'coinone',
    'coinspot',
    'coss',
    'crex24',
    'currencycom',
    'deribit',
    'digifinex',
    'dsx',
    'eterbase',
    'exmo',
    'exx',
    'fcoin',
    'fcoinjp',
    'flowbtc',
    'foxbit',
    'ftx',
    'gateio',
    'gemini',
    'hbtc',
    'hitbtc',
    'hollaex',
    'huobijp',
    'huobipro',
    'huobiru',
    'hyperliquid',
    'hyperliquid_abs',
    'hyperliquid_futures',
    'hyperliquid_spot',
    'ice3x',
    'idex',
    'independentreserve',
    'indodax',
    'itbit',
    'kraken',
    'kucoin',
    'kucoinfutures',
    'kuna',
    'lakebtc',
    'latoken',
    'lbank',
    'liquid',
    'livecoin',
    'luno',
    'lykke',
    'mercado',
    'mixcoins',
    'oceanex',
    'okcoin',
    'okx',
    'paymium',
    'phemex',
    'poloniex',
    'probit',
    'qtrade',
    'rightbtc',
    'southxchange',
    'stex',
    'stronghold',
    'surbitcoin',
    'therock',
    'tidebit',
    'tidex',
    'timex',
    'upbit',
    'vaultoro',
    'vbtc',
    'wavesexchange',
    'whitebit',
    'xbtce',
    'xena',
    'yobit',
    'zaif',
    'zb',
]

base = [
    'Exchange',
    'exchanges',
    'decimal_to_precision',
]

__all__ = base + errors.__all__ + exchanges
