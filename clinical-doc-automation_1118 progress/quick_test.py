#!/usr/bin/env python3
"""
Quick Test Script for User Guide Generator

快速測試腳本 - 一鍵生成使用者指南
"""

import sys
sys.path.insert(0, 'modules')

from user_guide_generator import (
    UserGuideGenerator,
    create_sample_protocol_info,
    create_sample_crf_design
)

def main():
    print("=" * 60)
    print("EDC/ePRO User Guide Generator - Quick Test")
    print("=" * 60)

    # 使用範例資料
    print("\n1. Creating sample data...")
    protocol_info = create_sample_protocol_info()
    crf_design = create_sample_crf_design()

    # 建立生成器
    print("2. Initializing generator...")
    generator = UserGuideGenerator(
        protocol_info=protocol_info,
        crf_design=crf_design,
        system_name="QuickTest EDC System"
    )

    # 生成使用者指南
    print("3. Generating user guide...\n")
    output_path = "output/quick_test_user_guide.docx"
    generator.generate(output_path)

    # 顯示結果
    print("\n" + "=" * 60)
    print("✓ Success! User guide generated.")
    print("=" * 60)
    print(f"\nOutput files:")
    print(f"  📄 Word Document: {output_path}")
    print(f"  📋 Screenshot List: {output_path.replace('.docx', '_screenshots.txt')}")
    print(f"\nStatistics:")
    print(f"  • Total screenshots needed: {len(generator.get_screenshot_list())}")
    print(f"  • Total forms: {len(crf_design['forms'])}")
    print(f"  • Protocol: {protocol_info['protocol_id']}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
