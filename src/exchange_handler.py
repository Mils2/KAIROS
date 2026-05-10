import ccxt


def get_exchange_connection(config):
    exchange_id = config.get("exchange", "binance")

    if exchange_id not in ccxt.exchanges:
        raise Exception(f"Exchange {exchange_id} not supported")

    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        "enableRateLimit": True,
        "rateLimit": 1200,
        "timeout": 30000,
    })
    return exchange


def fetch_price(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker["last"]


def fetch_ohlcv_data(exchange, symbol, timeframe="1h", limit=100):
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
