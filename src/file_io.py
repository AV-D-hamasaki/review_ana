from __future__ import annotations

from pathlib import Path
from typing import IO

import pandas as pd

REQUIRED_COLUMNS = ["id", "title", "rating", "content"]


def load_reviews(file: str | Path | IO) -> pd.DataFrame:
    """Load reviews from CSV or Excel file."""
    path = getattr(file, "name", file)
    if isinstance(path, (str, Path)) and str(path).lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return df


def save_to_excel(df: pd.DataFrame, path: str | Path | IO) -> None:
    """Save DataFrame to Excel."""
    df.to_excel(path, index=False)
