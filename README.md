# Review Visualization System

This project is a minimal example of a Streamlit app for labeling reviews with
needs and sentiment using the OpenAI API.

## Usage

1. Install dependencies (Streamlit, pandas, openpyxl). Because the environment
   might not have internet access, you may need to preinstall packages.
2. Run the Streamlit app:

```bash
streamlit run app.py
```

Upload a CSV or Excel file containing `id`, `title`, `rating`, and `content`
columns. After running labeling, metrics will be displayed and you can download
the labeled data as Excel.

The app works with both older and newer versions of the `openai` Python
package. Provide your API key via the `OPENAI_API_KEY` environment variable or
Streamlit `secrets.toml`.

For example, `.streamlit/secrets.toml` can contain:

```toml
openai_api_key = "sk-your-key"
```

Excel files are loaded using the `openpyxl` engine. If `openpyxl` is not
available at runtime, loading an Excel file will raise an informative error.
