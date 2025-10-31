import json
import os
import tempfile
from pathlib import Path

JSON_ENCODING = "utf-8"
JSON_ENSURE_ASCII = False
JSON_INDENT = 4


def dump_json(data: dict | list) -> str:
    return json.dumps(data, ensure_ascii=JSON_ENSURE_ASCII, indent=JSON_INDENT)


def read_json(path: Path) -> dict | list | None:
    if not path.exists():
        return
    with path.open("r", encoding=JSON_ENCODING) as f:
        return json.load(f)


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", delete=False, encoding=JSON_ENCODING, dir=str(path.parent)
    ) as tmp_file:
        json.dump(data, tmp_file, ensure_ascii=JSON_ENSURE_ASCII, indent=JSON_INDENT)
        tmp_file_path = Path(tmp_file.name)
    os.replace(tmp_file_path, path)
