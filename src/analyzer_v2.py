import requests

class BinanceAPIHandler:
    BASE_URL = "https://api.binance.com/api/v3"

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def get_price(self, symbol):
        endpoint = "/ticker/price"
        params = {"symbol": symbol.upper()}
        data = self._make_request(endpoint, params)
        if data and 'price' in data:
            try:
                return float(data['price'])
            except ValueError:
                return None
        return None

    def get_candles(self, symbol, interval, limit=500):
        endpoint = "/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": min(max(1, limit), 1000)
        }
        data = self._make_request(endpoint, params)
        return data