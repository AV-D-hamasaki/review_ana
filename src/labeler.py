from __future__ import annotations

import asyncio
import hashlib
from typing import Any, Dict, Iterable, List

import pandas as pd

try:
    import openai  # type: ignore
except Exception:  # pragma: no cover - openai optional
    openai = None

TOKEN_COST = 0.0  # placeholder cost per token


def _hash_review(row: pd.Series) -> str:
    m = hashlib.md5()
    m.update(str(row["id"]).encode())
    m.update(str(row["content"]).encode())
    return m.hexdigest()


def _dummy_label(content: str, needs: List[str]) -> Dict[str, Any]:
    # simple heuristic for offline demo
    need = needs[hash(content) % len(needs)] if needs else "unknown"
    sentiment = (
        "positive"
        if any(w in content.lower() for w in ["good", "great", "love"])
        else "negative"
    )
    return {
        "need": need,
        "sentiment": sentiment,
        "usage": {"total_tokens": len(content.split())},
    }


async def label_reviews(
    df: pd.DataFrame, needs: List[str], model: str = "gpt-3.5-turbo"
) -> pd.DataFrame:
    results = []
    for _, row in df.iterrows():
        h = _hash_review(row)
        if openai is None:
            result = _dummy_label(row["content"], needs)
        else:
            msg = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": row["content"]},
            ]
            resp = await openai.ChatCompletion.acreate(
                model=model, messages=msg, temperature=0
            )
            result = {
                "need": resp["choices"][0]["message"]["content"],
                "sentiment": "positive",  # placeholder
                "usage": resp["usage"],
            }
        results.append(result)
    new_df = df.copy()
    new_df["need"] = [r["need"] for r in results]
    new_df["sentiment"] = [r["sentiment"] for r in results]
    new_df["tokens"] = [r["usage"]["total_tokens"] for r in results]
    return new_df
