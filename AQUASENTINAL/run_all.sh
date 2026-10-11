#!/bin/bash
echo "==========================================="
echo "  AquaSentinel - Hackathon Startup Script"
echo "==========================================="

echo ""
echo "[1/4] Setting up environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "[2/4] Generating simulated datasets..."
python3 src/data_generator.py

echo ""
echo "[3/4] Training prediction model..."
python3 src/train_model.py

echo ""
echo "[4/4] Launching the AquaSentinel Dashboard..."
streamlit run app/main.py

echo "Done!"
