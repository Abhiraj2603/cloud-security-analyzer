#!/bin/bash

set -e

echo "========================================="
echo " Cloud Security Analyzer Installer"
echo "========================================="

# ---------------------------------------------------
# Check Python
# ---------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed."
    exit 1
fi

echo "✓ Python Found"

# ---------------------------------------------------
# Create Virtual Environment
# ---------------------------------------------------

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual Environment Created"
else
    echo "✓ Virtual Environment Already Exists"
fi

source venv/bin/activate

# ---------------------------------------------------
# Upgrade pip
# ---------------------------------------------------

pip install --upgrade pip

# ---------------------------------------------------
# Install Python Packages
# ---------------------------------------------------

echo "Installing Python dependencies..."

pip install -r requirements.txt

echo "✓ Python Packages Installed"

# ---------------------------------------------------
# AWS CLI
# ---------------------------------------------------

if command -v aws >/dev/null 2>&1; then
    echo "✓ AWS CLI Installed"
else
    echo ""
    echo "WARNING: AWS CLI is not installed."
    echo "Install AWS CLI before using this project."
fi

# ---------------------------------------------------
# Ollama
# ---------------------------------------------------

if command -v ollama >/dev/null 2>&1; then

    echo "✓ Ollama Installed"

else

    echo ""
    echo "Installing Ollama..."

    curl -fsSL https://ollama.com/install.sh | sh

fi

# ---------------------------------------------------
# Pull AI Model
# ---------------------------------------------------

echo "Checking Ollama model..."

ollama pull llama3.2

echo "✓ AI Model Ready"

# ---------------------------------------------------
# Check AWS Credentials
# ---------------------------------------------------

echo ""
echo "Checking AWS Credentials..."

if aws sts get-caller-identity >/dev/null 2>&1; then

    echo "✓ AWS Credentials Configured"

else

    echo ""
    echo "AWS credentials not found."

    echo ""

    aws configure

fi

# ---------------------------------------------------
# Finish
# ---------------------------------------------------

# ---------------------------------------------------
# Start Ollama
# ---------------------------------------------------

echo ""
echo "Starting Ollama..."

if pgrep -f "ollama serve" > /dev/null; then
    echo "✓ Ollama already running"
else
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
    echo "✓ Ollama started"
fi

# ---------------------------------------------------
# Start Flask
# ---------------------------------------------------

echo ""
echo "Starting Flask application..."

nohup python run.py >/tmp/cloud-security-analyzer.log 2>&1 &

sleep 5

echo ""
echo "========================================="
echo " Installation Completed Successfully!"
echo "========================================="
echo ""
echo "Application URL:"
echo ""
echo "http://127.0.0.1:5000"
echo ""
echo "Logs:"
echo "Ollama : /tmp/ollama.log"
echo "Flask  : /tmp/cloud-security-analyzer.log"
echo ""
