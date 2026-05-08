import pandas as pd

def process_data(ohlcv):
    """تحويل بيانات الشموع الخام إلى DataFrame منظم"""
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_sma(prices, window):
    """حساب المتوسط المتحرك البسيط"""
    if len(prices) < window:
        return None
    # استخدام pandas للحساب لضمان الدقة والسرعة
    return pd.Series(prices).rolling(window=window).mean().iloc[-1]

def calculate_rsi(prices, period=14):
    """حساب مؤشر القوة النسبية RSI"""
    if len(prices) < period + 1:
        return None
    
    delta = pd.Series(prices).diff()
    
    # حساب المكاسب والخسائر
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # حساب القوة النسبية
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

