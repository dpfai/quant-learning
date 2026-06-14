# Market Research Dashboard

A learning-focused market intelligence platform for visualization, risk
analysis, backtesting, and machine-learning experiments. It does not execute
real-money trades.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Optional AI summaries require `OPENAI_API_KEY`. All other features run without
an OpenAI account.

## Test

```bash
pytest
```

## Project Structure

- `app.py` - Main entry point
- `config/` - Configuration settings
- `data/` - Data storage (raw, processed, cache)
- `features/` - Feature engineering modules
- `pages/` - Streamlit multipage apps
- `utils/` - Utility functions
- `notebooks/` - Jupyter notebooks for exploration
- `tests/` - Unit tests

See [USER_GUIDE.md](USER_GUIDE.md) for page-level usage and methodology notes.
