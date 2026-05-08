import json
import os

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

def main():
    print("--- KAIROS Bot Starting ---")
    config = load_config()
    print(f"Monitoring: {config['symbols']}")
    # هنا سنضيف منطق التداول لاحقاً

if __name__ == "__main__":
    main()

