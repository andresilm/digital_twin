import json
import logging

logger = logging.getLogger(__name__)


def load_base_profile():
    base_profile = None
    try:
        with open("profile_data/base_profile.txt", "r", encoding="utf-8") as f:
            base_profile = f.read()
    except FileNotFoundError:
        logger.error('Base profile file not found')
    return base_profile


def load_profile_from_json():
    with open("profile_data/profile.json", "r", encoding="utf-8") as f:
        profile_json = json.load(f)
    profile_text = __json_to_text(profile_json)
    return profile_text


def __json_to_text(data, indent=0):
    text = ""
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            text += f"{prefix}{key}:\n"
            text += __json_to_text(value, indent + 1)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            text += f"{prefix}- "
            if isinstance(item, (dict, list)):
                text += "\n" + __json_to_text(item, indent + 1)
            else:
                text += f"{item}\n"
    else:
        text += f"{prefix}{data}\n"
    return text
