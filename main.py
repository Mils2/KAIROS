#!/usr/bin/env python3
import argparse
import logging
import signal
import sys

from src.settings import get_settings
from src.engine import run_bot
from src.telegram_utils import send_telegram_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/kairos.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

running = True

def signal_handler(sig, frame):
    global running
    running = False
    logger.info("Received signal %s, stopping...", sig)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="run", choices=["run", "health"])
    args = parser.parse_args()

    config = get_settings()

    if args.command == "health":
        logger.info(
            {
                "exchange": config["exchange"],
                "symbol": config["symbols"][0] if config["symbols"] else None,
                "telegram_token": bool(config["telegram"]["token"]),
                "telegram_chat_id": bool(config["telegram"]["chat_id"]),
                "risk_tp": config["risk"]["tp_percent"],
                "risk_sl": config["risk"]["sl_percent"],
            }
        )
        return

    send_telegram_message(
        config["telegram"]["token"],
        config["telegram"]["chat_id"],
        "KAIROS started successfully ✅"
    )

    logger.info("KAIROS starting...")
    run_bot(config)

if __name__ == "__main__":
    main()
