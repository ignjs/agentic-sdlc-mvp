from __future__ import annotations

from pathlib import Path


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def has_any_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def has_all_keywords(text: str, keywords: tuple[str, ...]) -> bool:
    return all(keyword in text for keyword in keywords)
