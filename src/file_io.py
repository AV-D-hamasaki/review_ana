from __future__ import annotations

from pathlib import Path
from typing import IO

import pandas as pd

REQUIRED_COLUMNS = ["id", "title", "rating", "content"]


def load_reviews(file: str | Path | IO) -> pd.DataFrame:
    """Load reviews from CSV or Excel file."""
    path = getattr(file, "name", file)
    if isinstance(path, (str, Path)) and str(path).lower().endswith(".csv"):
        # handle UTF-8 with BOM exported from Windows Excel
        df = pd.read_csv(file, encoding="utf-8-sig")
    else:
        try:
            df = pd.read_excel(file, engine="openpyxl")
        except ImportError as e:  # pragma: no cover - depends on environment
            raise ImportError(
                "Reading Excel files requires openpyxl. Please install openpyxl."
            ) from e
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return df


def save_to_excel(df: pd.DataFrame, path: str | Path | IO) -> None:
    """Save DataFrame to Excel."""
    df.to_excel(path, index=False)
