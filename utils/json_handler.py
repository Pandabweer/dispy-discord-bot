import json

from typing import Any

from core import logger


async def update_json(path: str, json_object: Any, indention: int = 4) -> None:
    with open(path, mode="r+") as file:
        file.write(json.dumps(json_object, indent=indention))
    logger.debug(f"Updated {path}")
