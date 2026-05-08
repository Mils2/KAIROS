import json
from src.exchange_handler import get_exchange_connection, fetch_price

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

def main():
    print("--- KAIROS Live Market Data ---")
    config = load_config()
    
    try:
        # إنشاء الاتصال
        exchange = get_exchange_connection(config)
        
        # جلب أسعار العملات المحددة في الإعدادات
        for symbol in config['symbols']:
            price = fetch_price(exchange, symbol)
            print(f"Current Price of {symbol}: {price}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

