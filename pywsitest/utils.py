import re
from typing import List


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
    resolved = _recurse_resolve(response, path)
    return [res for res in resolved if res is not None]


def _recurse_resolve(working: object, path: str) -> List[object]:
    resolved = []
    path = path.lstrip("/")

    if isinstance(working, list):
        resolved.extend(_resolve_index(working, path))
    else:
        resolved.extend(_resolve_path(working, path))

    return resolved


def _resolve_path(working: dict, path: str) -> List[object]:
    resolved = []

    match = WORD_REGEX.match(path)
    if not match:
        return resolved

    path = match.group(1)
    working = working.get(path)

    path = match.group(2)
    if path:
        resolved.extend(_recurse_resolve(working, path))
    else:
        resolved.append(working)

    return resolved


def _resolve_index(working: list, path: str) -> List[object]:
    resolved = []

    match = LIST_INDEX.match(path)
    if not match:
        return resolved

    index = match.group(1)
    path = match.group(2)

    if not index:
        for work in working:
            resolved.extend(_recurse_resolve(work, path))
        return resolved

    index = int(index)
    if len(working) > index:
        working = working[index]
        if path:
            resolved.extend(_recurse_resolve(working, path))
        else:
            resolved.append(working)

    return resolved
