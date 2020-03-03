import re
from typing import List, Tuple


PATH_REGEX = re.compile(r"^\$\{(.*)\}$")
ARRAY_REGEX = re.compile(r"^(.+?)\[(\d*)\](.*)$")

WORD_REGEX = re.compile(r"^([^\[\]\/]+)((\/|\[\d*\]).*)?$")
LIST_INDEX = re.compile(r"^\[(\d*)\](.*)$")


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


def get_resolved_values(response: [list, dict], path: str) -> List[object]:
    resolved = [response]

    for part in path.lstrip("/").split("/"):
        count = len(resolved)
        for i in range(count):
            current = resolved[i]
            if isinstance(current, dict):
                resolved[i] = current.get(part)
            elif isinstance(current, list):
                if part:
                    index, success = _to_int(part)
                    resolved[i] = current[index] if success and len(current) > index else None
                else:
                    for work in current:
                        resolved.append(work)
                    resolved[i] = None

        resolved = [r for r in resolved if r is not None]

    return resolved


def _to_int(value: str) -> Tuple[int, bool]:
    try:
        return int(value), True
    except ValueError:
        return 0, False
