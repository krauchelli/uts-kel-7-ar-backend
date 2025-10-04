@echo off
echo ============================================
echo Quick Virtual Environment Setup
echo Gender Detection Flask App
echo ============================================

echo.
echo This script will:
echo 1. Create virtual environment
echo 2. Activate it
echo 3. Install dependencies
echo 4. Run the Flask app
echo.

set /p confirm="Continue? (Y/n): "
if /i "%confirm%"=="n" exit

echo.
echo [1/4] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists, skipping creation...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!

echo.
echo [3/4] Installing/updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Trying manual installation...
    pip install Flask tensorflow opencv-python numpy Pillow
)
echo Dependencies installed!

echo.
echo [4/4] Checking model file...
if not exist "model\model.h5" (
    echo Warning: model\model.h5 not found!
    echo Please ensure your model file is in the model directory
    echo.
    set /p continue="Continue without model? (y/N): "
    if /i not "%continue%"=="y" (
        echo Setup completed. Add your model file and run: python app.py
        pause
        exit
    )
)

echo.
echo ============================================
echo Setup Complete! Starting Flask App...
echo ============================================
echo.
echo The app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py