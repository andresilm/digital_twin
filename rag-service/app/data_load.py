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
    profile_text = json_to_flat_text(profile_json)
    return profile_text


def json_to_flat_text(data, indent_level=0) -> str:
    """
    Converts a nested JSON object into plain text while preserving its hierarchical structure.

    Args:
        data (dict or list): The JSON object to flatten.
        indent_level (int): Current indentation level (used internally for recursion).

    Returns:
        str: A plain text representation of the JSON content.
    """
    lines = []
    indent = "  " * indent_level

    if isinstance(data, dict):
        for key, value in data.items():

            if indent_level <= 1:
                lines.append(f"{indent}{key.upper()}:")
            else:
                lines.append(f"{indent}{key}:")
            lines.append(json_to_flat_text(value, indent_level + 1))
    elif isinstance(data, list):
        for item in data:
            prefix = "- " if isinstance(item, (str, dict)) else ""
            nested = json_to_flat_text(item, indent_level + 1)
            if isinstance(item, str):
                lines.append(f"{indent}{prefix}{item}")
            else:
                lines.append(f"{indent}{prefix}{nested}")
    else:
        lines.append(f"{indent}{data}")

    return "\n".join([line for line in lines if line.strip()]) 





