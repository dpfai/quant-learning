# Market Research Dashboard

A research-oriented market intelligence platform.

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
