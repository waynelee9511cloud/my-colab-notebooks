#!/bin/bash

# 臨床試驗文件自動化系統 - Web UI 快速啟動腳本
# 作者: Clinical Data Automation Team
# 日期: 2025-11-18

echo "=================================================="
echo "臨床試驗文件自動化系統 - Web UI"
echo "Clinical Trial Document Automation System"
echo "=================================================="
echo ""

# 檢查 Python 是否已安裝
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null
then
    echo "❌ 錯誤: 找不到 Python"
    echo "請先安裝 Python 3.8 或以上版本"
    echo "下載地址: https://www.python.org/downloads/"
    exit 1
fi

# 使用 python3 或 python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "✓ 找到 Python: $($PYTHON_CMD --version)"
echo ""

# 檢查是否在專案目錄中
if [ ! -f "web_interface.py" ]; then
    echo "❌ 錯誤: 請在 clinical-doc-automation 目錄中執行此腳本"
    exit 1
fi

echo "✓ 專案目錄正確"
echo ""

# 檢查依賴套件
echo "檢查依賴套件..."

PACKAGES_OK=true

for package in gradio pdfplumber google-generativeai python-docx Pillow; do
    if ! $PYTHON_CMD -c "import $package" &> /dev/null; then
        echo "  ✗ $package 未安裝"
        PACKAGES_OK=false
    else
        echo "  ✓ $package 已安裝"
    fi
done

echo ""

if [ "$PACKAGES_OK" = false ]; then
    echo "⚠ 部分套件未安裝"
    echo ""
    echo "是否現在安裝? (y/n)"
    read -r response

    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo ""
        echo "安裝依賴套件..."
        $PYTHON_CMD -m pip install -r requirements.txt
        echo ""
        echo "✓ 依賴套件安裝完成"
        echo ""
    else
        echo ""
        echo "請手動安裝依賴套件:"
        echo "  $PYTHON_CMD -m pip install -r requirements.txt"
        echo ""
        exit 1
    fi
fi

# 創建輸出目錄
mkdir -p output
echo "✓ 輸出目錄已準備: output/"
echo ""

# 啟動 Web UI
echo "=================================================="
echo "正在啟動 Web UI..."
echo "=================================================="
echo ""
echo "啟動後請在瀏覽器中開啟顯示的網址"
echo ""
echo "按 Ctrl+C 可以停止服務"
echo ""
echo "=================================================="
echo ""

$PYTHON_CMD web_interface.py
