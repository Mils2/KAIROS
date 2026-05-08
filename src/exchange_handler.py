import ccxt

def get_exchange_connection(config):
    exchange_id = config.get('exchange', 'binance')
    
    # التأكد من وجود المنصة في مكتبة ccxt
    if exchange_id in ccxt.exchanges:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'enableRateLimit': True, # ضروري لتجنب الحظر من المنصة
        })
        return exchange
    else:
        raise Exception(f"Exchange {exchange_id} not supported")

def fetch_price(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']
