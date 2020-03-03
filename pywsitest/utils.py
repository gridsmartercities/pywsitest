import re
from typing import List, Tuple


PATH_REGEX = re.compile(r"^\$\{(.*)\}$")


def get_resolved_values(response: [list, dict], path: str) -> List[object]:
    """
    Retrieves a list of values from a dictionary at a given path

    Parameters:
        response (list, dict): The response to check against for values
        path (str): The path in the response to check for values

    Returns:
        (list[object]): The list of objects at a given path, empty if the path can't be found
    """
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
