"""
Web UI 測試腳本

此腳本用於測試 Web UI 的基本功能是否正常運作。

作者: Clinical Data Automation Team
日期: 2025-11-18
"""

import sys
import os
from pathlib import Path

# 添加專案路徑
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """測試模組導入"""
    print("=" * 80)
    print("測試 1: 模組導入")
    print("=" * 80)

    tests = {
        "gradio": "Gradio Web 框架",
        "pdfplumber": "PDF 處理",
        "google.generativeai": "Google Gemini API",
        "docx": "Word 文件處理 (python-docx)",
        "PIL": "圖片處理 (Pillow)",
    }

    all_passed = True

    for module_name, description in tests.items():
        try:
            __import__(module_name)
            print(f"  ✓ {description:40} [{module_name}]")
        except ImportError as e:
            print(f"  ✗ {description:40} [{module_name}]")
            print(f"    錯誤: {e}")
            all_passed = False

    print()
    if all_passed:
        print("✅ 所有必要的套件都已安裝")
    else:
        print("❌ 部分套件缺失，請執行: pip install -r requirements.txt")

    print()
    return all_passed


def test_project_modules():
    """測試專案模組"""
    print("=" * 80)
    print("測試 2: 專案模組")
    print("=" * 80)

    modules = {
        "modules.protocol_parser": "Protocol Parser",
        "modules.crf_generator": "CRF Generator",
        "modules.dvp_generator": "DVP Generator",
        "modules.user_guide_generator": "User Guide Generator",
        "modules.word_formatter": "Word Formatter",
    }

    all_passed = True

    for module_name, description in modules.items():
        try:
            __import__(module_name)
            print(f"  ✓ {description:40} [{module_name}]")
        except ImportError as e:
            print(f"  ✗ {description:40} [{module_name}]")
            print(f"    錯誤: {e}")
            all_passed = False

    print()
    if all_passed:
        print("✅ 所有專案模組都可以正常導入")
    else:
        print("❌ 部分模組導入失敗，請檢查檔案是否存在")

    print()
    return all_passed


def test_web_interface():
    """測試 Web UI 模組"""
    print("=" * 80)
    print("測試 3: Web UI 模組")
    print("=" * 80)

    try:
        from web_interface import ClinicalDocWebUI
        print("  ✓ Web UI 模組導入成功")

        # 創建實例
        web_ui = ClinicalDocWebUI()
        print("  ✓ Web UI 實例創建成功")

        # 檢查關鍵方法
        methods = [
            "upload_pdf",
            "upload_logo",
            "set_api_key",
            "parse_protocol",
            "update_protocol_info",
            "generate_documents",
            "create_interface",
            "launch"
        ]

        for method in methods:
            if hasattr(web_ui, method):
                print(f"    ✓ 方法 {method} 存在")
            else:
                print(f"    ✗ 方法 {method} 缺失")
                return False

        print()
        print("✅ Web UI 模組正常運作")
        print()
        return True

    except Exception as e:
        print(f"  ✗ Web UI 模組測試失敗")
        print(f"    錯誤: {e}")
        print()
        print("❌ Web UI 模組無法正常運作")
        print()
        return False


def test_file_structure():
    """測試專案檔案結構"""
    print("=" * 80)
    print("測試 4: 專案檔案結構")
    print("=" * 80)

    required_files = {
        "web_interface.py": "Web UI 主程式",
        "requirements.txt": "依賴套件清單",
        "modules/protocol_parser.py": "Protocol Parser 模組",
        "modules/crf_generator.py": "CRF Generator 模組",
        "modules/dvp_generator.py": "DVP Generator 模組",
        "modules/user_guide_generator.py": "User Guide Generator 模組",
        "modules/word_formatter.py": "Word Formatter 模組",
        "WEB_UI_README.md": "Web UI 使用文檔",
        "WEB_UI_QUICKSTART.md": "快速開始指南",
        "examples/Web_UI_Demo.ipynb": "Colab 示範筆記本",
    }

    all_passed = True

    for file_path, description in required_files.items():
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size / 1024  # KB
            print(f"  ✓ {description:40} [{file_path}] ({size:.1f} KB)")
        else:
            print(f"  ✗ {description:40} [{file_path}] (缺失)")
            all_passed = False

    # 檢查目錄
    print()
    print("檢查目錄結構:")

    directories = ["modules", "templates", "utils", "output", "examples"]

    for directory in directories:
        path = Path(directory)
        if path.exists() and path.is_dir():
            print(f"  ✓ {directory}/ 目錄存在")
        else:
            status = "不存在" if not path.exists() else "不是目錄"
            print(f"  ℹ {directory}/ 目錄 {status} (可選)")

    print()
    if all_passed:
        print("✅ 所有必要檔案都存在")
    else:
        print("❌ 部分檔案缺失")

    print()
    return all_passed


def test_api_connection():
    """測試 API 連線（僅檢查模組，不實際調用）"""
    print("=" * 80)
    print("測試 5: API 連線能力")
    print("=" * 80)

    try:
        import google.generativeai as genai
        print("  ✓ Google Gemini API 模組已安裝")

        # 檢查環境變數（不檢查實際值）
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print("  ℹ 環境變數 GEMINI_API_KEY 已設定")
            print("    (實際連線需要在 Web UI 中測試)")
        else:
            print("  ℹ 環境變數 GEMINI_API_KEY 未設定")
            print("    (可在 Web UI 中手動設定)")

        print()
        print("✅ API 連線能力正常（需在 Web UI 中實際測試）")
        print()
        return True

    except Exception as e:
        print(f"  ✗ API 連線測試失敗")
        print(f"    錯誤: {e}")
        print()
        print("❌ API 連線能力異常")
        print()
        return False


def test_gradio_version():
    """測試 Gradio 版本"""
    print("=" * 80)
    print("測試 6: Gradio 版本")
    print("=" * 80)

    try:
        import gradio as gr
        version = gr.__version__
        print(f"  ✓ Gradio 版本: {version}")

        # 檢查版本是否符合要求（4.0.0 或以上）
        major_version = int(version.split('.')[0])
        if major_version >= 4:
            print(f"  ✓ 版本符合要求（>= 4.0.0）")
            print()
            print("✅ Gradio 版本正常")
        else:
            print(f"  ⚠ 版本過舊（< 4.0.0）")
            print(f"  建議升級: pip install --upgrade gradio")
            print()
            print("⚠️ Gradio 版本過舊，建議升級")

        print()
        return True

    except Exception as e:
        print(f"  ✗ Gradio 版本檢查失敗")
        print(f"    錯誤: {e}")
        print()
        print("❌ Gradio 版本檢查異常")
        print()
        return False


def run_all_tests():
    """執行所有測試"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Web UI 系統測試" + " " * 44 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    results = {
        "模組導入": test_imports(),
        "專案模組": test_project_modules(),
        "Web UI 模組": test_web_interface(),
        "檔案結構": test_file_structure(),
        "API 連線能力": test_api_connection(),
        "Gradio 版本": test_gradio_version(),
    }

    # 總結
    print("=" * 80)
    print("測試總結")
    print("=" * 80)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {status:10} {test_name}")

    print()
    print(f"總計: {passed}/{total} 項測試通過")
    print()

    if passed == total:
        print("🎉 恭喜！所有測試都通過了！")
        print()
        print("您可以開始使用 Web UI:")
        print("  - 執行: python web_interface.py")
        print("  - 或執行啟動腳本: ./launch_web_ui.sh (Linux/Mac)")
        print("  - 或執行啟動腳本: launch_web_ui.bat (Windows)")
        print()
        return True
    else:
        print("⚠️ 部分測試失敗，請根據上述訊息進行修復。")
        print()
        print("常見解決方法:")
        print("  1. 安裝缺失的套件: pip install -r requirements.txt")
        print("  2. 檢查專案檔案是否完整")
        print("  3. 確認在正確的目錄中執行測試")
        print()
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n測試被中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n測試執行時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
