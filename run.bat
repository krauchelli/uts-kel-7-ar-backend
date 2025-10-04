@echo off
echo ============================================
echo Starting Gender Detection Flask App
echo ============================================

echo.
echo Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found
    echo Please run setup.bat first or ensure you have the dependencies installed
    echo.
)

echo.
echo Checking model file...
if not exist "model\model.h5" (
    echo Error: Model file 'model\model.h5' not found
    echo Please ensure your model file is placed in the model directory
    pause
    exit /b 1
)

echo.
echo Starting Flask application...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py