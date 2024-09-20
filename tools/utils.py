import json
import logging
import os
import re

from aiogram import types

logger = logging.getLogger(__name__)


class JSONObject:
    def __init__(self, dic):
        vars(self).update(dic)


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf8') as cfg_file:
            return json.load(cfg_file, object_hook=JSONObject)
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_path}")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the config file: {config_path}")
    return None


config = load_config()

SPAM_LINKS_REGEX = re.compile(r"(https?:\/\/)?(t\.me|waxu|binance|xyz)", re.IGNORECASE)
group_id = ""


def is_spam(message: types.Message):
    return bool(message.text and SPAM_LINKS_REGEX.search(message.text))
