import io
import pandas as pd
import pytest
from src import file_io


def test_load_reviews_csv(tmp_path):
    df = pd.DataFrame({
        "id": [1],
        "title": ["a"],
        "rating": [5],
        "content": ["good"],
    })
    path = tmp_path / "r.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    loaded = file_io.load_reviews(path.open("r", encoding="utf-8-sig"))
    pd.testing.assert_frame_equal(df, loaded)


def test_load_reviews_excel_requires_openpyxl():
    fake = io.BytesIO()
    fake.name = "r.xlsx"
    with pytest.raises(ImportError):
        file_io.load_reviews(fake)
