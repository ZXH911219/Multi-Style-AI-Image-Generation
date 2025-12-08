@echo off
REM Streamlit Application Launcher
REM 多風格 AI 繪圖生成器 - Streamlit 應用啟動腳本

echo.
echo ======================================================================
echo   多風格 AI 繪圖生成器 - Streamlit 應用啟動
echo   Multi-Style AI Image Generator - Streamlit Web App Launcher
echo ======================================================================
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Streamlit 未安裝!
    echo 請先運行: pip install streamlit
    echo.
    pause
    exit /b 1
)

REM Change to project directory
cd /d "c:\Users\user\Desktop\HW4"

REM Check if streamlit_app.py exists
if not exist "streamlit_app.py" (
    echo.
    echo ERROR: streamlit_app.py 文件未找到!
    echo 請確保文件位於: c:\Users\user\Desktop\HW4\
    echo.
    pause
    exit /b 1
)

echo.
echo 正在啟動 Streamlit 應用...
echo 應用將在瀏覽器中打開: http://localhost:8501
echo.
echo 按 Ctrl+C 停止應用
echo.

REM Launch streamlit app
python -m streamlit run streamlit_app.py

pause
