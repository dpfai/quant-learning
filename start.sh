#!/bin/bash
# Quant Learning Dashboard Startup Script

# Project directory
PROJECT_DIR="/Users/lobster/AI-workplace/quant-learning"
cd "$PROJECT_DIR"

# Load environment variables
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

# Activate virtual environment and start Streamlit
source "$PROJECT_DIR/venv/bin/activate"
streamlit run app.py --server.port 8501 --server.headless true
