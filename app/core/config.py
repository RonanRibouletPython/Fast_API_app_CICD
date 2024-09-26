import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        raise Exception(f"Config file not found at {CONFIG_PATH}")
    except json.JSONDecodeError:
        raise Exception("Config file is not a valid JSON")

config = load_config()