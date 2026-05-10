import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config" / "config.json"

def _load_json_config():
    if CONFIG_PATH.exists():
        text = CONFIG_PATH.read_text(encoding="utf-8")
        return json.loads(text)
    return {}

def get_settings():
    file_cfg = _load_json_config()
    telegram_cfg = file_cfg.get("telegram", {})
    risk_cfg = file_cfg.get("risk", {})
    runtime_cfg = file_cfg.get("runtime", {})

    exchange = os.getenv("BINANCE_EXCHANGE", file_cfg.get("exchange", "binance"))
    symbol = os.getenv("BOT_SYMBOL", "")
    symbols = [symbol] if symbol else file_cfg.get("symbols", ["BTC/USDT"])

    return {
        "exchange": exchange,
        "symbols": symbols,
        "telegram": {
            "token": os.getenv("TELEGRAM_BOT_TOKEN", telegram_cfg.get("token", "")),
            "chat_id": os.getenv("TELEGRAM_CHAT_ID", str(telegram_cfg.get("chat_id", ""))),
        },
        "risk": {
            "tp_percent": float(os.getenv("TP_PERCENT", risk_cfg.get("tp_percent", 2.0))),
            "sl_percent": float(os.getenv("SL_PERCENT", risk_cfg.get("sl_percent", 1.0))),
        },
        "runtime": {
            "timeframe": os.getenv("TIMEFRAME", runtime_cfg.get("timeframe", "1h")),
            "poll_seconds": int(os.getenv("POLL_SECONDS", runtime_cfg.get("poll_seconds", 30))),
        }
    }
