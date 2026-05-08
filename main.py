import json
import time
import os
from src.exchange_handler import get_exchange_connection
from src.analyzer import process_data, calculate_sma, calculate_rsi

def load_config():
    """تحميل الإعدادات من ملف config.json"""
    with open('config/config.json', 'r') as f:
        return json.load(f)

def main():
    print("--- KAIROS Advanced Analysis Mode ---")
    
    # 1. تحميل الإعدادات والاتصال بالمنصة
    try:
        config = load_config()
        exchange = get_exchange_connection(config)
        symbol = config['symbols'][0] # BTC/USDT
        print(f"Monitoring: {symbol} in real-time...\n")
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    # 2. حلقة التشغيل اللانهائية للتحليل
    while True:
        try:
            # جلب آخر 50 شمعة (لضمان دقة RSI و SMA20)
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=50)
            df = process_data(ohlcv)
            
            # حساب القيم الحالية
            current_price = df['close'].iloc[-1]
            sma_20 = calculate_sma(df['close'].tolist(), 20)
            rsi = calculate_rsi(df['close'].tolist())
            
            # طباعة النتائج في سطر واحد منظم
            output = f"{symbol} | Price: {current_price:<10} | SMA20: {sma_20:>10.2f} | RSI: {rsi:>6.2f}"
            print(output)
            
            # منطق التنبيهات (Signals)
            if rsi:
                if rsi > 70:
                    print("   ⚠️  STATUS: Overbought - High Risk of Reversal!")
                elif rsi < 30:
                    print("   ✅  STATUS: Oversold - Potential Buying Opportunity!")
                
                # ربط السعر بالمتوسط المتحرك
                if current_price > sma_20 and rsi < 60:
                    print("   📈  TREND: Strong Bullish (Price > SMA & Healthy RSI)")
                elif current_price < sma_20 and rsi > 40:
                    print("   📉  TREND: Strong Bearish (Price < SMA & Weak RSI)")

            # الانتظار لمدة 15 ثانية قبل التحديث القادم
            time.sleep(15)
            
        except KeyboardInterrupt:
            print("\n--- KAIROS Paused by User ---")
            break
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()

