from __future__ import annotations

import pandas as pd


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Return metrics aggregated by need."""
    if "need" not in df.columns or "sentiment" not in df.columns:
        raise ValueError("DataFrame must contain 'need' and 'sentiment' columns")
    total = len(df)
    grouped = df.groupby("need")
    need_share = grouped.size() / total
    positive_rate = grouped.apply(lambda g: (g["sentiment"] == "positive").mean())
    frustration_index = (1 - positive_rate) * need_share
    metrics = pd.DataFrame(
        {
            "Need Share": need_share,
            "Positive Rate": positive_rate,
            "Frustration Index": frustration_index,
        }
    )
    return metrics.sort_values("Need Share", ascending=False)
