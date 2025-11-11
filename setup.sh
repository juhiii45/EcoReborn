#!/bin/bash
# Ecoreborn Website - Linux/Mac Setup Script
# This script automates the initial setup process

set -e

echo "========================================"
echo "Ecoreborn Website Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo "[1/6] Checking Python version..."
python3 --version

echo ""
echo "[2/6] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists, skipping creation"
else
    python3 -m venv .venv
    echo "Virtual environment created successfully"
fi

echo ""
echo "[3/6] Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "[4/6] Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "[5/6] Setting up environment configuration..."
if [ -f ".env" ]; then
    echo ".env file already exists, skipping"
else
    cp .env.example .env
    echo ".env file created. Please edit it with your MongoDB credentials."
fi

echo ""
echo "[6/6] Setup complete!"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Edit .env file and add your MongoDB Atlas credentials"
echo "2. Run: python init_db.py"
echo "3. Run: python app.py"
echo "4. Open http://localhost:5000 in your browser"
echo ""
echo "Default admin credentials:"
echo "  Email: admin@ecoreborn.example"
echo "  Password: Ec0r3b0rn!"
echo ""
echo "========================================"
echo ""
