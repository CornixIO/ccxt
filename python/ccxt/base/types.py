import sys
import types
from typing import Union, List, Optional, Any
from decimal import Decimal


if sys.version_info.minor >= 8:
    from typing import TypedDict, Literal, Dict
else:
    from typing import Dict
    from typing_extensions import Literal
    TypedDict = Dict

if sys.version_info.minor >= 11:
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


OrderSide = Literal['buy', 'sell']
OrderType = Literal['limit', 'market']
PositionSide = Literal['long', 'short']


class Entry:
    def __init__(self, path, api, method, config):
        self.name = None
        self.path = path
        self.api = api
        self.method = method
        self.config = config

        def unbound_method(_self, params={}):
            return _self.request(self.path, self.api, self.method, params, config=self.config)

        self.unbound_method = unbound_method

    def __get__(self, instance, owner):
        if instance is None:
            return self.unbound_method
        else:
            return types.MethodType(self.unbound_method, instance)

    def __set_name__(self, owner, name):
        self.name = name


IndexType = Union[str, int]
Num = Union[None, str, float, int, Decimal]
Str = Optional[str]
Strings = Optional[List[str]]
Int = Optional[int]
Bool = Optional[bool]
MarketType = Literal['spot', 'margin', 'swap', 'future', 'option']


class FeeInterface(TypedDict):
    currency: Str
    cost: Num
    rate: NotRequired[Num]


Fee = Optional[FeeInterface]


class TradingFeeInterface(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    maker: Num
    taker: Num
    percentage: Bool
    tierBased: Bool


class Balance(TypedDict):
    free: Num
    used: Num
    total: Num
    debt: NotRequired[Num]


class Account(TypedDict):
    free: Str
    used: Str
    total: Str


class Trade(TypedDict):
    info: Dict[str, Any]
    amount: Num
    datetime: Str
    id: Str
    order: Str
    price: Num
    timestamp: Int
    type: Str
    side: Str
    symbol: Str
    takerOrMaker: Str
    cost: Num
    fee: Fee


class Position(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    id: Str
    timestamp: Int
    datetime: Str
    contracts: Num
    contractSize: Num
    side: Str
    notional: Num
    leverage: Num
    unrealizedPnl: Num
    realizedPnl: Num
    collateral: Num
    entryPrice: Num
    markPrice: Num
    liquidationPrice: Num
    hedged: bool
    maintenanceMargin: Num
    initialMargin: Num
    initialMarginPercentage: Num
    marginMode: Str
    marginRatio: Num
    lastUpdateTimestamp: Int
    lastPrice: Num
    percentage: Num
    stopLossPrice: Num
    takeProfitPrice: Num


class OrderRequest(TypedDict):
    symbol: Str
    type: Str
    side: Str
    amount: Union[None, float]
    price: Union[None, float]
    params: Dict[str, Any]


class Order(TypedDict):
    info: Dict[str, Any]
    id: Str
    clientOrderId: Str
    datetime: Str
    timestamp: Int
    lastTradeTimestamp: Int
    lastUpdateTimestamp: Int
    status: Str
    symbol: Str
    type: Str
    timeInForce: Str
    side: OrderSide
    price: Num
    average: Num
    amount: Num
    filled: Num
    remaining: Num
    stopPrice: Num
    takeProfitPrice: Num
    stopLossPrice: Num
    cost: Num
    trades: List[Trade]
    fee: Fee

class Liquidation(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    timestamp: Int
    datetime: Str
    price: Num
    baseValue: Num
    quoteValue: Num

class FundingHistory(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    code: Str
    timestamp: Int
    datetime: Str
    id: Str
    amount: Num


class Balances(Dict[str, Balance]):
    datetime: Str
    timestamp: Int


class OrderBook(TypedDict):
    asks: List[Num]
    bids: List[Num]
    datetime: Str
    timestamp: Int
    nonce: Int


class Transaction(TypedDict):
    info: Dict[str, any]
    id: Str
    txid: Str
    timestamp: Int
    datetime: Str
    address: Str
    addressFrom: Str
    addressTo: Str
    tag: Str
    tagFrom: Str
    tagTo: Str
    type: Str
    amount: Num
    currency: Str
    status: Str
    updated: Int
    fee: Fee
    network: Str
    comment: Str
    internal: Bool


class TransferEntry(TypedDict):
    info: Dict[str, any]
    id: Str
    timestamp: Int
    datetime: Str
    currency: Str
    amount: Num
    fromAccount: Str
    toAccount: Str
    status: Str


class Ticker(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    timestamp: Int
    datetime: Str
    high: Num
    low: Num
    bid: Num
    bidVolume: Num
    ask: Num
    askVolume: Num
    vwap: Num
    open: Num
    close: Num
    last: Num
    previousClose: Num
    change: Num
    percentage: Num
    average: Num
    quoteVolume: Num
    baseVolume: Num


Tickers = Dict[str, Ticker]


class MarginMode(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    marginMode: Str


class Leverage(TypedDict):
    info: Dict[str, Any]
    symbol: Str
    marginMode: Str
    longLeverage: Num
    shortLeverage: Num


class Greeks(TypedDict):
    symbol: Str
    timestamp: Int
    datetime: Str
    delta: Num
    gamma: Num
    theta: Num
    vega: Num
    rho: Num
    bidSize: Num
    askSize: Num
    bidImpliedVolatility: Num
    askImpliedVolatility: Num
    markImpliedVolatility: Num
    bidPrice: Num
    askPrice: Num
    markPrice: Num
    lastPrice: Num
    underlyingPrice: Num
    info: Dict[str, Any]


class MarketInterface(TypedDict):
    info: Dict[str, Any]
    id: Str
    symbol: Str
    base: Str
    quote: Str
    baseId: Str
    quoteId: Str
    active: Bool
    type: Str
    subType: Str
    spot: bool
    margin: bool
    swap: bool
    future: bool
    option: bool
    contract: bool
    settle: Str
    settleId: Str
    contractSize: Num
    linear: bool
    inverse: bool
    expiry: Num
    expiryDatetime: Str
    strike: Num
    optionType: Str
    taker: Num
    maker: Num
    percentage: bool
    tierBased: bool
    feeSide: Str
    precision: Any
    limits: Any
    created: Int


class CurrencyInterface(TypedDict):
    id: Str
    code: Str
    precision: Num


class LastPrice(TypedDict):
    symbol: Str
    timestamp: Int
    datetime: Str
    price: Num
    side: OrderSide
    info: Dict[str, Any]


class CrossBorrowRate(TypedDict):
    info: Dict[str, any]
    currency: Str
    rate: float
    period: Optional[float]
    timestamp: Int
    datetime: Str


class IsolatedBorrowRate(TypedDict):
    info: Dict[str, any]
    symbol: str
    base: str
    baseRate: float
    quote: str
    quoteRate: float
    period: Int
    timestamp: Int
    datetime: Str


class FundingRate(TypedDict):
    symbol: Str
    timestamp: Int
    fundingRate: Num
    datetime: Str
    markPrice: Num
    indexPrice: Num
    interestRate: Num
    estimatedSettlePrice: Num
    fundingTimestamp: Int
    fundingDatetime: Str
    nextFundingTimestamp: Int
    nextFundingDatetime: Str
    nextFundingRate: Num
    previousFundingTimestamp: Int
    previousFundingDatetime: Str
    previousFundingRate: Num
    info: Dict[str, Any]
    interval: Str


class CancellationRequest(TypedDict):
    id: Str
    symbol: Str
    clientOrderId: Str


class MarginModification(TypedDict):
    info: Dict[str, any]
    symbol: str
    type: Optional[Literal['add', 'reduce', 'set']]
    marginMode: Optional[Literal['isolated', 'cross']]
    amount: Optional[float]
    code: Str
    status: Str
    timestamp: Int
    datetime: Str


class LeverageTier:
    tier: Num
    symbol: Str
    currency: Str
    minNotional: Num
    maxNotional: Num
    maintenanceMarginRate: Num
    maxLeverage: Num
    info: Dict[str, Any]


class LedgerEntry:
    id: Str
    info: Any
    timestamp: Int
    datetime: Str
    direction: Str
    account: Str
    referenceId: Str
    referenceAccount: Str
    type: Str
    currency: Str
    amount: Str
    before: float
    after: float
    status: Str
    fee: Fee


class DepositAddress:
    info: Any
    currency: Str
    network: Optional[Str]
    address: Str
    tag: Optional[Str]


LastPrices = Dict[Str, LastPrice]
Currencies = Dict[Str, CurrencyInterface]
TradingFees = Dict[Str, TradingFeeInterface]

Market = Optional[MarketInterface]
Currency = Optional[CurrencyInterface]

FundingRates = Dict[Str, FundingRate]
IsolatedBorrowRates = Dict[Str, IsolatedBorrowRate]
CrossBorrowRates = Dict[Str, CrossBorrowRate]
LeverageTiers = Dict[Str, List[LeverageTier]]
