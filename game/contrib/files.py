from pathlib import Path
import json

__all__ = (
    'del_extension',
    'load_json',
    'save_json',
)


def del_extension(filename: str) -> str:
    return filename.split('.')[0]


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(path: Path, json_: dict) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        return json.dump(json_, file, indent=4, ensure_ascii=False)
