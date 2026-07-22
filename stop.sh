#!/bin/bash

echo "Stopping Cloud Security Analyzer..."

pkill -f "python run.py" || true
pkill -f "ollama serve" || true

echo "✓ Application stopped."
