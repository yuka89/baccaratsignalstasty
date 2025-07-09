#!/bin/bash
echo "Installing Python dependencies..."
pip install fastapi uvicorn

echo "Starting AI Trading Assistant..."
echo "Open your browser to: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo "=" * 50

python simple_version.py