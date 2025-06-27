import json
import logging

logger = logging.getLogger(__name__)


def load_base_profile():
    """
    Loads the base profile text from a local file.

    Reads the contents of 'profile_data/base_profile.txt' as a UTF-8 encoded string.

    Returns:
        str or None: The content of the base profile file if found, otherwise None.

    Logs an error if the file is not found.
    """
    base_profile = None
    try:
        with open("profile_data/base_profile.txt", "r", encoding="utf-8") as f:
            base_profile = f.read()
    except FileNotFoundError:
        logger.error('Base profile file not found')
    return base_profile


def load_profile_from_json():
    """
    Loads a profile from a JSON file and converts it to a formatted text representation.

    Reads 'profile_data/profile.json', parses the JSON content,
    then converts it into an indented text format using __json_to_text.

    Returns:
        str: The formatted text representation of the profile JSON.
    """
    with open("profile_data/profile.json", "r", encoding="utf-8") as f:
        profile_json = json.load(f)
    profile_text = __json_to_text(profile_json)
    return profile_text


def __json_to_text(data, indent=0):
    """
    Recursively converts JSON-like data (dicts, lists, primitives) into a formatted
    indented text representation.

    Args:
        data (dict, list, or primitive): The input JSON-like data to convert.
        indent (int): Current indentation level (number of indent steps).

    Returns:
        str: The formatted multiline string representing the JSON structure.

    Behavior:
        - Dictionaries are printed as:
            key:
              nested_key:
                ...
        - Lists are printed with a dash prefix:
            - item1
            - item2
              nested_key:
                ...
        - Primitive values (str, int, etc.) are printed directly with indentation.

    Efficiency:
        Uses list appends and ''.join() to efficiently concatenate strings
        rather than repeated += operations.
    """
    lines = []
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            lines.append(f"{prefix}{key}:\n")
            lines.append(__json_to_text(value, indent + 1))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}- \n")
                lines.append(__json_to_text(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}\n")
    else:
        lines.append(f"{prefix}{data}\n")

    return ''.join(lines)

