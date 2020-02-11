import re


PATH_REGEX = re.compile(r"^\$\{(.*)\}$")


def get_resolved_value(response: dict, path: str) -> object:
    """
    Retrieves a value from a dictionary at a given path

    Parameters:
        response (dict): The response to check against for a value
        path (str): The path in the response to check for a value

    Returns:
        (object): The object at a given path, or None if the path can't be found
    """
    resolved = response
    for part in path.split("/"):
        if part not in resolved:
            return None
        resolved = resolved[part]
    return resolved
