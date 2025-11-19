"""
Word文件格式化引擎快速測試
快速驗證模組是否正常運作
"""

import sys
import os

# 添加模組路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.word_formatter import WordFormatter, create_clinical_document
from datetime import datetime


def quick_test():
    """快速測試基本功能"""
    print("\n" + "=" * 60)
    print("Word文件格式化引擎 - 快速測試")
    print("=" * 60)

    try:
        # 確保輸出目錄存在
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✓ 已建立輸出目錄: {output_dir}")

        # 測試1: 基本文件建立
        print("\n測試1: 建立基本文件...")
        formatter = WordFormatter()
        formatter.create_document()
        formatter.set_page_format()
        print("✓ 文件建立成功")

        # 測試2: 設定頁首頁尾
        print("\n測試2: 設定頁首頁尾...")
        formatter.set_header(
            document_title="Test Protocol",
            protocol_number="TEST-001",
            version="1.0"
        )
        formatter.set_footer()
        print("✓ 頁首頁尾設定成功")

        # 測試3: 添加內容
        print("\n測試3: 添加內容...")
        formatter.apply_title_style("1. Test Section", level=1)
        formatter.apply_body_style("This is a test document created on " + datetime.now().strftime('%Y-%m-%d'))
        print("✓ 內容添加成功")

        # 測試4: 建立表格
        print("\n測試4: 建立表格...")
        table = formatter.doc.add_table(rows=3, cols=2)
        formatter.apply_table_style(table)
        table.rows[0].cells[0].text = 'Item'
        table.rows[0].cells[1].text = 'Value'
        table.rows[1].cells[0].text = 'Test 1'
        table.rows[1].cells[1].text = 'Pass'
        table.rows[2].cells[0].text = 'Test 2'
        table.rows[2].cells[1].text = 'Pass'
        print("✓ 表格建立成功")

        # 測試5: 儲存文件
        print("\n測試5: 儲存文件...")
        output_path = os.path.join(output_dir, 'quick_test.docx')
        formatter.save_document(output_path)
        print(f"✓ 文件已儲存至: {output_path}")

        # 測試6: 使用便利函數
        print("\n測試6: 使用便利函數建立完整文件...")
        output_path_2 = os.path.join(output_dir, 'quick_test_complete.docx')
        formatter2 = create_clinical_document(
            document_title="Quick Test Protocol",
            protocol_number="QT-2025-001",
            version="1.0",
            sponsor="Test Pharmaceutical",
            indication="Testing",
            output_path=output_path_2
        )
        formatter2.apply_title_style("1. INTRODUCTION", level=1)
        formatter2.apply_body_style("This is a quick test of the complete document creation function.")
        formatter2.save_document(output_path_2)
        print(f"✓ 完整文件已儲存至: {output_path_2}")

        # 測試總結
        print("\n" + "=" * 60)
        print("測試結果：全部通過 ✓")
        print("=" * 60)
        print(f"\n生成的測試文件：")
        print(f"1. {output_path}")
        print(f"2. {output_path_2}")
        print("\n您可以開啟這些文件檢查格式是否正確。")

        return True

    except Exception as e:
        print(f"\n✗ 測試失敗：{str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
