@echo off
REM 臨床試驗文件自動化系統 - Web UI 快速啟動腳本 (Windows)
REM 作者: Clinical Data Automation Team
REM 日期: 2025-11-18

echo ==================================================
echo 臨床試驗文件自動化系統 - Web UI
echo Clinical Trial Document Automation System
echo ==================================================
echo.

REM 檢查 Python 是否已安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 錯誤: 找不到 Python
    echo 請先安裝 Python 3.8 或以上版本
    echo 下載地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ 找到 Python: %PYTHON_VERSION%
echo.

REM 檢查是否在專案目錄中
if not exist "web_interface.py" (
    echo ❌ 錯誤: 請在 clinical-doc-automation 目錄中執行此腳本
    pause
    exit /b 1
)

echo ✓ 專案目錄正確
echo.

REM 檢查依賴套件
echo 檢查依賴套件...

set PACKAGES_OK=true

python -c "import gradio" >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ gradio 未安裝
    set PACKAGES_OK=false
) else (
    echo   ✓ gradio 已安裝
)

python -c "import pdfplumber" >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ pdfplumber 未安裝
    set PACKAGES_OK=false
) else (
    echo   ✓ pdfplumber 已安裝
)

python -c "import google.generativeai" >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ google-generativeai 未安裝
    set PACKAGES_OK=false
) else (
    echo   ✓ google-generativeai 已安裝
)

python -c "import docx" >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ python-docx 未安裝
    set PACKAGES_OK=false
) else (
    echo   ✓ python-docx 已安裝
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ Pillow 未安裝
    set PACKAGES_OK=false
) else (
    echo   ✓ Pillow 已安裝
)

echo.

if "%PACKAGES_OK%"=="false" (
    echo ⚠ 部分套件未安裝
    echo.
    set /p INSTALL="是否現在安裝? (Y/N): "

    if /i "%INSTALL%"=="Y" (
        echo.
        echo 安裝依賴套件...
        python -m pip install -r requirements.txt
        echo.
        echo ✓ 依賴套件安裝完成
        echo.
    ) else (
        echo.
        echo 請手動安裝依賴套件:
        echo   python -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM 創建輸出目錄
if not exist "output" mkdir output
echo ✓ 輸出目錄已準備: output\
echo.

REM 啟動 Web UI
echo ==================================================
echo 正在啟動 Web UI...
echo ==================================================
echo.
echo 啟動後請在瀏覽器中開啟顯示的網址
echo.
echo 按 Ctrl+C 可以停止服務
echo.
echo ==================================================
echo.

python web_interface.py

pause
