import time
import logging

from src.exchange_handler import get_exchange_connection, fetch_ohlcv_data
from src.analyzer import process_data, calculate_sma, calculate_rsi
from src.notifier import send_telegram_message

logger = logging.getLogger(__name__)
logger.propagate = False
NL = chr(10)


def notify(config, text):
    try:
        token = config["telegram"]["token"]
        chat_id = config["telegram"]["chat_id"]
        if token and chat_id:
            send_telegram_message(token, chat_id, text)
    except Exception as e:
        logger.error("Telegram notification failed: %s", e)


def run_bot(config):
    symbol = config["symbols"][0]
    timeframe = config["runtime"]["timeframe"]
    poll_seconds = config["runtime"]["poll_seconds"]
    tp_percent = config["risk"]["tp_percent"]
    sl_percent = config["risk"]["sl_percent"]

    exchange = get_exchange_connection(config)

    in_position = False
    entry_price = None

    logger.info("KAIROS starting...")
    print("KAIROS starting...")
    print("Config loaded: symbol=%s, timeframe=%s" % (symbol, timeframe))
    print("Exchange connected: %s" % config["exchange"])

    while True:
        try:
            print("Fetching OHLCV...")
            ohlcv = fetch_ohlcv_data(exchange, symbol, timeframe=timeframe, limit=50)
            print("Fetched candles: %s" % len(ohlcv))

            df = process_data(ohlcv)
            print("Processed dataframe OK")

            close_prices = df["close"].astype(float).tolist()
            price = close_prices[-1]
            sma20 = calculate_sma(close_prices, 20)
            rsi = calculate_rsi(close_prices, 14)

            print("Price=%s | RSI=%s | SMA20=%s | in_position=%s" % (price, rsi, sma20, in_position))

            if sma20 is None or rsi is None:
                print("Not enough data for indicators.")
                print("Sleeping %ss..." % poll_seconds)
                time.sleep(poll_seconds)
                continue

            entry_signal = (not in_position) and (price > sma20 and rsi < 70)
            close_signal = in_position and (
                price >= entry_price * (1 + tp_percent / 100)
                or price <= entry_price * (1 - sl_percent / 100)
            )

            if entry_signal:
                logger.info("Entry signal detected.")
                print("Entry signal detected.")
                notify(
                    config,
                    NL.join([
                        "Entry signal detected",
                        "Symbol: %s" % symbol,
                        "Price: %s" % price,
                        "RSI: %s" % rsi,
                        "SMA20: %s" % sma20,
                    ])
                )

                in_position = True
                entry_price = price

                logger.info("Order opened at %s", entry_price)
                print("Order opened at %s" % entry_price)
                notify(
                    config,
                    NL.join([
                        "Order opened",
                        "Symbol: %s" % symbol,
                        "Entry price: %s" % entry_price,
                        "TP: %s%%" % tp_percent,
                        "SL: %s%%" % sl_percent,
                    ])
                )

            elif close_signal:
                logger.info("Order closed at %s", price)
                print("Order closed at %s" % price)
                notify(
                    config,
                    NL.join([
                        "Order closed",
                        "Symbol: %s" % symbol,
                        "Close price: %s" % price,
                        "Entry price: %s" % entry_price,
                    ])
                )

                in_position = False
                entry_price = None

            else:
                print("No entry signal.")

            print("Sleeping %ss..." % poll_seconds)
            time.sleep(poll_seconds)

        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            print("Bot stopped by user.")
            notify(config, "KAIROS stopped by user.")
            break

        except Exception as e:
            logger.exception("Error occurred: %s", e)
            print("Error occurred: %s" % e)
            notify(config, "Error occurred" + NL + str(e))
            time.sleep(poll_seconds)
