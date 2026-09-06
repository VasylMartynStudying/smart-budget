from pathlib import Path

STYLESHEET_PATH = Path(__file__).resolve().parent / "styles.qss"


def load_stylesheet() -> str:
    return STYLESHEET_PATH.read_text(encoding="utf-8")
