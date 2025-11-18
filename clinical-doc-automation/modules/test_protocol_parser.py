"""
Protocol Parser 模組測試腳本

此腳本用於驗證 Protocol Parser 模組的基本功能
"""

import os
import sys
from pathlib import Path

def test_imports():
    """測試模組導入"""
    print("測試 1: 檢查模組導入...")
    try:
        from protocol_parser import ProtocolParser, ProtocolInfo
        print("  ✓ ProtocolParser 導入成功")
        print("  ✓ ProtocolInfo 導入成功")
        return True
    except ImportError as e:
        print(f"  ✗ 導入失敗: {e}")
        return False


def test_dependencies():
    """測試依賴套件"""
    print("\n測試 2: 檢查依賴套件...")

    dependencies = {
        "pdfplumber": "PDF 處理",
        "google.generativeai": "Gemini AI",
    }

    all_ok = True
    for module_name, description in dependencies.items():
        try:
            __import__(module_name)
            print(f"  ✓ {description:15} ({module_name})")
        except ImportError:
            print(f"  ✗ {description:15} ({module_name}) - 需要安裝")
            all_ok = False

    return all_ok


def test_parser_initialization():
    """測試解析器初始化"""
    print("\n測試 3: 測試解析器初始化...")
    try:
        from protocol_parser import ProtocolParser

        # 測試無 API 金鑰初始化（應該會有警告但不會報錯）
        parser = ProtocolParser()
        print("  ✓ 無 API 金鑰初始化成功（會有警告）")

        # 測試有 API 金鑰初始化
        parser = ProtocolParser(api_key="test_key_12345")
        print("  ✓ 有 API 金鑰初始化成功")

        return True
    except Exception as e:
        print(f"  ✗ 初始化失敗: {e}")
        return False


def test_protocol_info():
    """測試 ProtocolInfo 資料結構"""
    print("\n測試 4: 測試 ProtocolInfo 資料結構...")
    try:
        from protocol_parser import ProtocolInfo

        # 創建測試資料
        info = ProtocolInfo(
            study_title="Test Study",
            protocol_number="TEST-001",
            sponsor="Test Sponsor",
            phase="Phase III",
            crf_domains=["Demographics", "Vital Signs"]
        )

        # 測試 to_dict
        data_dict = info.to_dict()
        assert isinstance(data_dict, dict)
        assert data_dict["study_title"] == "Test Study"
        print("  ✓ to_dict() 功能正常")

        # 測試 to_json
        json_str = info.to_json()
        assert isinstance(json_str, str)
        assert "Test Study" in json_str
        print("  ✓ to_json() 功能正常")

        return True
    except Exception as e:
        print(f"  ✗ 測試失敗: {e}")
        return False


def test_pdf_text_extraction():
    """測試 PDF 文本提取（需要測試 PDF）"""
    print("\n測試 5: 測試 PDF 文本提取...")
    try:
        from protocol_parser import ProtocolParser

        parser = ProtocolParser(api_key="test_key")

        # 檢查是否有測試 PDF
        test_pdf_paths = [
            "test_protocol.pdf",
            "../test_protocol.pdf",
            "../../test_protocol.pdf"
        ]

        test_pdf = None
        for path in test_pdf_paths:
            if Path(path).exists():
                test_pdf = path
                break

        if test_pdf:
            text = parser.extract_text_from_pdf(test_pdf, max_pages=1)
            assert isinstance(text, str)
            assert len(text) > 0
            print(f"  ✓ PDF 文本提取成功 (提取了 {len(text)} 字元)")
            return True
        else:
            print("  ⊘ 跳過 (未找到測試 PDF 檔案)")
            return True

    except Exception as e:
        print(f"  ✗ 測試失敗: {e}")
        return False


def test_api_configuration():
    """測試 API 配置"""
    print("\n測試 6: 測試 API 配置...")
    try:
        from protocol_parser import ProtocolParser
        import google.generativeai as genai

        # 測試環境變數配置
        test_key = "test_api_key_12345"
        os.environ["GEMINI_API_KEY"] = test_key

        parser = ProtocolParser()
        assert parser.api_key == test_key
        print("  ✓ 環境變數配置正常")

        # 測試直接傳入配置
        parser = ProtocolParser(api_key="another_test_key")
        assert parser.api_key == "another_test_key"
        print("  ✓ 直接傳入配置正常")

        # 清理環境變數
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

        return True
    except Exception as e:
        print(f"  ✗ 測試失敗: {e}")
        return False


def main():
    """主測試函數"""
    print("=" * 80)
    print("Protocol Parser 模組測試")
    print("=" * 80)

    tests = [
        test_imports,
        test_dependencies,
        test_parser_initialization,
        test_protocol_info,
        test_pdf_text_extraction,
        test_api_configuration,
    ]

    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)

    # 總結
    print("\n" + "=" * 80)
    print("測試總結")
    print("=" * 80)

    passed = sum(results)
    total = len(results)

    print(f"\n通過: {passed}/{total}")

    if passed == total:
        print("\n✓ 所有測試通過！模組可以正常使用。")
        return 0
    else:
        print("\n⚠ 部分測試未通過，請檢查上方的錯誤訊息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
