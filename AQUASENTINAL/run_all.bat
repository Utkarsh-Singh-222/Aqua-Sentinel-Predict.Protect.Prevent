@echo off
echo ===========================================
echo   AquaSentinel - Hackathon Startup Script
echo ===========================================

echo.
echo [1/4] Setting up environment...
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo [2/4] Generating simulated datasets...
python src\data_generator.py

echo.
echo [3/4] Training prediction model...
python src\train_model.py

echo.
echo [4/4] Launching the AquaSentinel Dashboard...
python -m streamlit run app\main.py

echo Done!
