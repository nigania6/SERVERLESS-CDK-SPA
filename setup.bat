@echo off
REM Setup script for Windows
echo ====================================
echo Weather Pipeline - Stage 1 Setup
echo ====================================
echo.

REM Check if Python 3 is installed
REM Try python3 first, then fallback to python (Windows often uses just 'python')
python3 --version >nul 2>&1
if errorlevel 1 (
    REM Try python command as fallback
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python 3 is not installed or not in PATH
        echo Please install Python 3.9 or higher
        exit /b 1
    )
    set PYTHON_CMD=python
    echo Using 'python' command
) else (
    set PYTHON_CMD=python3
    echo Using 'python3' command
)

REM Verify it's Python 3.9 or higher
%PYTHON_CMD% -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.9 or higher is required
    echo Current version:
    %PYTHON_CMD% --version
    exit /b 1
)
echo Detected Python version:
%PYTHON_CMD% --version

echo [1/5] Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo [5/5] Checking AWS CLI...
aws --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: AWS CLI is not installed or not in PATH
    echo Please install AWS CLI and configure credentials
) else (
    echo AWS CLI is installed
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Make sure AWS credentials are configured: aws configure
echo 2. Bootstrap CDK (first time only): cdk bootstrap
echo 3. Deploy the stack: cdk deploy
echo.
echo To activate the virtual environment in the future, run:
echo   venv\Scripts\activate.bat
echo.

pause

