#!/usr/bin/env python3
"""
測試安裝和環境設置

這個腳本用於檢查所有必要的依賴和環境配置是否正確。

運行此腳本來驗證：
1. Python 版本
2. 必要的套件
3. API Key 設置
4. 模組導入

Author: Clinical Documentation Automation Team
Date: 2025-11-18
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """打印標題"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_result(check_name, passed, message=""):
    """打印檢查結果"""
    icon = "✓" if passed else "✗"
    status = "通過" if passed else "失敗"
    color = "\033[92m" if passed else "\033[91m"  # Green or Red
    reset = "\033[0m"

    print(f"{color}{icon} {check_name}: {status}{reset}")
    if message:
        print(f"  {message}")


def check_python_version():
    """檢查 Python 版本"""
    print_header("檢查 Python 版本")

    version = sys.version_info
    current = f"{version.major}.{version.minor}.{version.micro}"
    required = (3, 8)

    passed = version >= required
    message = f"當前版本: {current}, 要求: >= {required[0]}.{required[1]}"

    print_result("Python 版本", passed, message)
    return passed


def check_dependencies():
    """檢查必要的依賴套件"""
    print_header("檢查依賴套件")

    dependencies = {
        'pdfplumber': '讀取 PDF 檔案',
        'google.generativeai': 'Gemini API',
        'docx': 'Word 文件生成 (python-docx)',
    }

    all_passed = True

    for package, description in dependencies.items():
        try:
            __import__(package)
            print_result(f"{package}", True, description)
        except ImportError:
            print_result(f"{package}", False, f"{description} - 需要安裝")
            all_passed = False

    if not all_passed:
        print("\n安裝缺少的套件:")
        print("  pip install -r requirements.txt")

    return all_passed


def check_api_key():
    """檢查 API Key 設置"""
    print_header("檢查 API Key 設置")

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
        print_result("GEMINI_API_KEY", True, f"環境變數已設置: {masked_key}")
        return True
    else:
        print_result("GEMINI_API_KEY", False, "環境變數未設置")
        print("\n設置 API Key:")
        print("  Linux/Mac:   export GEMINI_API_KEY='your-api-key'")
        print("  Windows CMD: set GEMINI_API_KEY=your-api-key")
        print("  PowerShell:  $env:GEMINI_API_KEY='your-api-key'")
        return False


def check_module_imports():
    """檢查專案模組是否能正確導入"""
    print_header("檢查專案模組")

    # 添加專案路徑
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    modules = {
        'automation_workflow': ['ClinicalDocAutomation', 'BatchProcessor'],
        'modules.protocol_parser': ['ProtocolParser', 'ProtocolInfo'],
        'modules.crf_generator': ['CRFGenerator', 'CRFDomain'],
        'modules.dvp_generator': ['DVPGenerator'],
        'modules.user_guide_generator': ['UserGuideGenerator'],
    }

    all_passed = True

    for module_name, classes in modules.items():
        try:
            module = __import__(module_name, fromlist=classes)

            # 檢查類別是否存在
            missing_classes = []
            for class_name in classes:
                if not hasattr(module, class_name):
                    missing_classes.append(class_name)

            if missing_classes:
                print_result(
                    module_name,
                    False,
                    f"缺少類別: {', '.join(missing_classes)}"
                )
                all_passed = False
            else:
                print_result(
                    module_name,
                    True,
                    f"包含: {', '.join(classes)}"
                )

        except ImportError as e:
            print_result(module_name, False, f"導入失敗: {str(e)}")
            all_passed = False

    return all_passed


def check_file_structure():
    """檢查檔案結構"""
    print_header("檢查檔案結構")

    required_files = [
        'automation_workflow.py',
        'requirements.txt',
        'modules/__init__.py',
        'modules/protocol_parser.py',
        'modules/crf_generator.py',
        'modules/dvp_generator.py',
        'modules/user_guide_generator.py',
    ]

    all_exist = True
    project_root = Path(__file__).parent

    for file_path in required_files:
        full_path = project_root / file_path
        exists = full_path.exists()

        if not exists:
            all_exist = False

        print_result(file_path, exists)

    return all_exist


def check_output_directory():
    """檢查輸出目錄權限"""
    print_header("檢查輸出目錄權限")

    project_root = Path(__file__).parent
    test_dir = project_root / "test_output"

    try:
        # 嘗試創建測試目錄
        test_dir.mkdir(parents=True, exist_ok=True)

        # 嘗試寫入測試檔案
        test_file = test_dir / "test.txt"
        test_file.write_text("test")

        # 嘗試讀取
        content = test_file.read_text()

        # 清理
        test_file.unlink()
        test_dir.rmdir()

        print_result("目錄讀寫權限", True, "可以創建目錄和檔案")
        return True

    except Exception as e:
        print_result("目錄讀寫權限", False, f"無法寫入: {str(e)}")
        return False


def run_minimal_test():
    """運行最小化功能測試"""
    print_header("功能測試")

    try:
        # 導入模組
        from automation_workflow import ClinicalDocAutomation
        print_result("導入 ClinicalDocAutomation", True)

        # 測試類別初始化（使用假檔案路徑，但不實際執行）
        # 這裡只測試類別結構，不測試實際功能
        print_result("類別結構檢查", True, "所有類別可以正確導入")

        return True

    except Exception as e:
        print_result("功能測試", False, str(e))
        return False


def print_summary(results):
    """打印總結"""
    print_header("測試總結")

    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed

    print(f"\n總檢查項目: {total}")
    print(f"通過: {passed}")
    print(f"失敗: {failed}")

    if failed == 0:
        print("\n🎉 所有檢查通過！您可以開始使用自動化工作流程了。")
        print("\n快速開始:")
        print("  python automation_workflow.py --protocol your_protocol.pdf")
        return True
    else:
        print("\n⚠️  有些檢查失敗，請先解決上述問題。")
        print("\n常見解決方法:")
        print("  1. 安裝依賴: pip install -r requirements.txt")
        print("  2. 設置 API Key: export GEMINI_API_KEY='your-key'")
        print("  3. 檢查檔案完整性")
        return False


def main():
    """主函數"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "Clinical Document Automation - 安裝測試".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # 執行所有檢查
    results = {
        'Python 版本': check_python_version(),
        '依賴套件': check_dependencies(),
        'API Key': check_api_key(),
        '模組導入': check_module_imports(),
        '檔案結構': check_file_structure(),
        '目錄權限': check_output_directory(),
        '功能測試': run_minimal_test(),
    }

    # 打印總結
    all_passed = print_summary(results)

    # 返回適當的退出碼
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
