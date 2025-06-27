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


def json_to_flat_text(data, prefix_path=None):
    """
    Recursively flattens a nested JSON-like structure into a plain text string.
    Each line contains the full path from the root to an object, with grouped leaves for lists of primitives or dicts.

    Args:
        data (dict, list, or primitive): The JSON-like structure to flatten.
        prefix_path (list): Accumulator for the current path of keys.

    Returns:
        str: A multiline string where each line represents a grouped object or list.
    """
    if prefix_path is None:
        prefix_path = []

    lines = []

    # Handle dictionary objects by iterating key-value pairs
    if isinstance(data, dict):
        current_line = []
        for key, value in data.items():
            # If the value is nested (dict or list), recursively flatten it
            if isinstance(value, (dict, list)):
                lines.append(json_to_flat_text(value, prefix_path + [key]))
            else:
                # Collect simple key-value pairs to form a grouped line
                current_line.append(f"{key}: {value}")
        # If there are simple key-value pairs, join them in one line with the current path as prefix
        if current_line:
            full_path = " > ".join(prefix_path)
            lines.append(f"{full_path} | " + " | ".join(current_line))

    # Handle list objects
    elif isinstance(data, list):
        # If the list consists entirely of dictionaries, flatten each dict separately
        if all(isinstance(item, dict) for item in data):
            for item in data:
                lines.append(json_to_flat_text(item, prefix_path))
        # If the list contains only primitive types, join them in one line
        elif all(isinstance(item, (str, int, float)) for item in data):
            full_path = " > ".join(prefix_path)
            joined = ", ".join(str(x) for x in data)
            lines.append(f"{full_path} > {joined}")
        else:
            # For mixed or complex lists, recursively process each item individually
            for item in data:
                lines.append(json_to_flat_text(item, prefix_path))

    # Base case: the data is a primitive value (str, int, float, etc.)
    else:
        full_path = " > ".join(prefix_path)
        lines.append(f"{full_path} > {data}")

    # Join all lines into a single string separated by newlines, filtering out any empty lines
    result = "\n".join([line for line in lines if line.strip()])
    logger.debug(result)
    return result




