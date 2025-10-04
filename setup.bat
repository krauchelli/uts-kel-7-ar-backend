@echo off
echo ============================================
echo Gender Detection Flask App Setup
echo ============================================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
echo Trying with exact versions first...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Failed with exact versions. Trying manual installation...
    pip install Flask tensorflow opencv-python numpy Pillow
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies
        echo.
        echo Possible solutions:
        echo 1. Update Python to version 3.9-3.11
        echo 2. Try: pip install --upgrade pip
        echo 3. Try: pip install tensorflow-cpu (if you don't need GPU)
        echo 4. Install Visual C++ Build Tools
        pause
        exit /b 1
    ) else (
        echo Manual installation successful!
    )
) else (
    echo Exact version installation successful!
)

echo.
echo Checking model file...
if not exist "model\model.h5" (
    echo Warning: Model file 'model\model.h5' not found
    echo Please ensure your model file is placed in the model directory
    pause
)

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the app: python app.py
echo 3. Open browser: http://localhost:5000
echo.
pause