import pandas as pd


def process_data(ohlcv):
    df = pd.DataFrame(
        ohlcv,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def calculate_sma(prices, window):
    if len(prices) < window:
        return None
    relevant_prices = prices[-window:]
    return sum(relevant_prices) / window


def calculate_ema(prices, window):
    if len(prices) < window:
        return None

    ema_values = []
    sma_first_window = sum(prices[:window]) / window
    ema_values.append(sma_first_window)

    multiplier = 2 / (window + 1)

    for i in range(window, len(prices)):
        current_price = prices[i]
        prev_ema = ema_values[-1]
        current_ema = (current_price - prev_ema) * multiplier + prev_ema
        ema_values.append(current_ema)

    return ema_values


def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None

    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [abs(delta) if delta < 0 else 0 for delta in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    if len(prices) < slow_period:
        return None, None, None

    ema_fast_series = calculate_ema(prices, fast_period)
    ema_slow_series = calculate_ema(prices, slow_period)

    if ema_fast_series is None or ema_slow_series is None:
        return None, None, None

    start_offset_fast = slow_period - fast_period
    macd_line_series = []

    for i in range(len(ema_slow_series)):
        macd_line_val = ema_fast_series[start_offset_fast + i] - ema_slow_series[i]
        macd_line_series.append(macd_line_val)

    if len(macd_line_series) < signal_period:
        return None, None, None

    signal_line_series = calculate_ema(macd_line_series, signal_period)

    if signal_line_series is None:
        return None, None, None

    start_offset_macd_for_histogram = signal_period - 1
    histogram_series = []

    for i in range(len(signal_line_series)):
        histogram_val = macd_line_series[start_offset_macd_for_histogram + i] - signal_line_series[i]
        histogram_series.append(histogram_val)

    return macd_line_series[-1], signal_line_series[-1], histogram_series[-1]
