#!/bin/bash

echo "Starting Cloud Security Analyzer..."

# Activate virtual environment
source venv/bin/activate

# Start Ollama if not already running
if pgrep -f "ollama serve" >/dev/null; then
    echo "✓ Ollama already running"
else
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
    echo "✓ Ollama started"
fi

# Start Flask
nohup python run.py >/tmp/cloud-security-analyzer.log 2>&1 &

sleep 2

echo ""
echo "Application Started!"
echo ""
echo "Dashboard:"
echo "http://127.0.0.1:5000"
echo ""
echo "Logs:"
echo "/tmp/cloud-security-analyzer.log"
