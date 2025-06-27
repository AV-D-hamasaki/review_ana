import asyncio
import pandas as pd

from src import labeler


def test_label_reviews_dummy(monkeypatch):
    """label_reviews falls back to dummy labeling when openai is missing."""
    monkeypatch.setattr(labeler, "openai", None)

    df = pd.DataFrame({
        "id": [1],
        "title": ["a"],
        "rating": [5],
        "content": ["good"],
    })

    labeled = asyncio.run(labeler.label_reviews(df, ["design"]))

    assert labeled.loc[0, "need"] == "design"
    assert labeled.loc[0, "sentiment"] == "positive"
    assert labeled.loc[0, "tokens"] > 0
