# Review Visualization System

This project is a minimal example of a Streamlit app for labeling reviews with
needs and sentiment using the OpenAI API.

## Usage

1. Install dependencies (Streamlit, pandas). Because the environment might not
   have internet access, you may need to preinstall packages.
2. Run the Streamlit app:

```bash
streamlit run app.py
```

Upload a CSV or Excel file containing `id`, `title`, `rating`, and `content`
columns. After running labeling, metrics will be displayed and you can download
the labeled data as Excel.
