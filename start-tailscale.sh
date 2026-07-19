#!/bin/bash
# Quant Learning Dashboard - Tailscale HTTPS

PROJECT_DIR="/Users/lobster/AI-workplace/quant-learning"
cd "$PROJECT_DIR"

# Load environment variables
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

# Start with Tailscale IP
source "$PROJECT_DIR/venv/bin/activate"
streamlit run app.py \
  --server.port 8501 \
  --server.address 100.67.207.80 \
  --server.headless true
