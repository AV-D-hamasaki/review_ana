from __future__ import annotations

import json
from pathlib import Path
from typing import List

MASTER_PATH = Path("needs_master.json")


def load_master(path: Path = MASTER_PATH) -> List[str]:
    if path.exists():
        return json.loads(path.read_text())
    return []


def save_master(needs: List[str], path: Path = MASTER_PATH) -> None:
    path.write_text(json.dumps(needs, ensure_ascii=False, indent=2))
