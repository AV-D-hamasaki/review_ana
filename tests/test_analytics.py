import pandas as pd

from src import analytics


def test_calculate_metrics():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "title": ["a", "b", "c"],
            "rating": [5, 4, 2],
            "content": ["good", "bad", "good"],
            "need": ["design", "design", "price"],
            "sentiment": ["positive", "negative", "positive"],
        }
    )
    metrics = analytics.calculate_metrics(df)
    assert "Need Share" in metrics.columns
    assert metrics.loc["design", "Positive Rate"] == 0.5
