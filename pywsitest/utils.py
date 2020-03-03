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
    resolved = _recurse_resolve(response, path.lstrip("/"))
    return [res for res in resolved if res is not None]


def _recurse_resolve(working: object, path: str) -> List[object]:
    if not path:
        return [working]

    if isinstance(working, list):
        return _resolve_index(working, path)

    if isinstance(working, dict):
        return _resolve_path(working, path)

    return []


def _to_int(value: str) -> Tuple[int, bool]:
    try:
        return int(value), True
    except ValueError:
        return 0, False


def _resolve_path(working: dict, path: str) -> List[object]:
    resolved = []

    paths = path.split("/", 1)

    if not paths[0]:
        return resolved

    working = working.get(paths[0])

    if len(paths) > 1:
        resolved.extend(_recurse_resolve(working, paths[1]))
    else:
        resolved.append(working)

    return resolved


def _resolve_index(working: list, path: str) -> List[object]:
    resolved = []

    paths = path.split("/", 1)

    if paths[0]:
        index, success = _to_int(paths[0])
        if not success or len(working) <= index:
            return resolved

        working = working[index]

        if len(paths) > 1:
            resolved.extend(_recurse_resolve(working, paths[1]))
        else:
            resolved.append(working)
    else:
        if len(paths) > 1:
            for work in working:
                resolved.extend(_recurse_resolve(work, paths[1]))
        else:
            for work in working:
                resolved.append(work)

    return resolved
