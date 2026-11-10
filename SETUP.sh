#!/bin/bash

echo "🚀 Portfolio Optimization Dashboard Setup"
echo "=========================================="
echo ""

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 To run the dashboard:"
echo "   streamlit run app.py"
echo ""
echo "📖 For quick start guide:"
echo "   cat QUICKSTART.md"
echo ""
echo "Happy analyzing! 📊"
