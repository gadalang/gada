__all__ = ["_set", "_print", "_max", "_min"]


def _set(inputs: dict) -> dict:
    return {"out": inputs.get("in", None)}


def _print(inputs: dict) -> dict:
    if "in" in inputs:
        print(inputs["in"])

    return {}


def _max(inputs: dict) -> dict:
    return {"out": max(inputs.get("a", None), inputs.get("b", None))}


def _min(inputs: dict) -> dict:
    return {"out": min(inputs.get("a", None), inputs.get("b", None))}
