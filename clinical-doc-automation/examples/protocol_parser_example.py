"""
Protocol Parser 完整使用範例

此腳本展示如何使用 ProtocolParser 模組來解析臨床試驗 Protocol PDF 檔案
"""

import sys
import os
from pathlib import Path

# 添加模組路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.protocol_parser import ProtocolParser, ProtocolInfo


def main():
    """主函數"""
    print("=" * 80)
    print("Protocol PDF 解析器 - 完整範例")
    print("=" * 80)

    # ========== 配置設定 ==========
    # 方式1: 使用環境變數（推薦）
    # export GEMINI_API_KEY="your-api-key-here"

    # 方式2: 直接設置（僅供測試）
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

    # PDF 檔案路徑（請替換為實際路徑）
    PDF_PATH = "path/to/your/protocol.pdf"

    # 輸出路徑
    OUTPUT_DIR = Path(__file__).parent.parent / "output"
    OUTPUT_DIR.mkdir(exist_ok=True)

    # ========== 初始化解析器 ==========
    print("\n1. 初始化 Protocol 解析器...")
    try:
        parser = ProtocolParser(
            api_key=GEMINI_API_KEY,
            model_name="gemini-1.5-flash"  # 使用免費的 Flash 模型
        )
        print("   ✓ 解析器初始化成功")
    except Exception as e:
        print(f"   ✗ 初始化失敗: {e}")
        return

    # ========== 解析 Protocol PDF ==========
    print(f"\n2. 解析 Protocol PDF: {PDF_PATH}")

    if not Path(PDF_PATH).exists():
        print(f"   ✗ PDF 檔案不存在")
        print(f"\n   請修改 PDF_PATH 變數為實際的 PDF 檔案路徑")
        print(f"   當前路徑: {Path(PDF_PATH).absolute()}")
        return

    try:
        # 解析 Protocol（可選擇只讀取前N頁以加快速度）
        protocol_info = parser.parse_protocol(
            pdf_path=PDF_PATH,
            max_pages=None  # None = 讀取全部頁面，或設置如 50 只讀前50頁
        )
        print("   ✓ Protocol 解析完成")
    except Exception as e:
        print(f"   ✗ 解析失敗: {e}")
        import traceback
        traceback.print_exc()
        return

    # ========== 顯示提取的資訊 ==========
    print("\n" + "=" * 80)
    print("提取的 Protocol 資訊")
    print("=" * 80)

    # 基本資訊
    print("\n【基本資訊】")
    print(f"試驗標題: {protocol_info.study_title or 'N/A'}")
    print(f"Protocol 編號: {protocol_info.protocol_number or 'N/A'}")
    print(f"贊助商: {protocol_info.sponsor or 'N/A'}")
    print(f"試驗階段: {protocol_info.phase or 'N/A'}")

    # 試驗設計
    print("\n【試驗設計】")
    print(f"設計類型: {protocol_info.study_design or 'N/A'}")
    print(f"目標族群: {protocol_info.target_population or 'N/A'}")
    print(f"樣本數: {protocol_info.sample_size or 'N/A'}")

    # 訪視時程
    print("\n【訪視時程】")
    if protocol_info.visit_schedule:
        for i, visit in enumerate(protocol_info.visit_schedule, 1):
            print(f"  {i}. {visit}")
    else:
        print("  未提取到訪視時程")

    # 終點指標
    print("\n【主要終點指標】")
    if protocol_info.primary_endpoints:
        for i, endpoint in enumerate(protocol_info.primary_endpoints, 1):
            print(f"  {i}. {endpoint}")
    else:
        print("  未提取到主要終點指標")

    print("\n【次要終點指標】")
    if protocol_info.secondary_endpoints:
        for i, endpoint in enumerate(protocol_info.secondary_endpoints, 1):
            print(f"  {i}. {endpoint}")
    else:
        print("  未提取到次要終點指標")

    # 納入/排除標準
    print("\n【納入標準】")
    if protocol_info.inclusion_criteria:
        for i, criterion in enumerate(protocol_info.inclusion_criteria[:10], 1):
            print(f"  {i}. {criterion}")
        if len(protocol_info.inclusion_criteria) > 10:
            print(f"  ... 還有 {len(protocol_info.inclusion_criteria) - 10} 項")
    else:
        print("  未提取到納入標準")

    print("\n【排除標準】")
    if protocol_info.exclusion_criteria:
        for i, criterion in enumerate(protocol_info.exclusion_criteria[:10], 1):
            print(f"  {i}. {criterion}")
        if len(protocol_info.exclusion_criteria) > 10:
            print(f"  ... 還有 {len(protocol_info.exclusion_criteria) - 10} 項")
    else:
        print("  未提取到排除標準")

    # CRF 領域
    print("\n【所需 CRF 領域】")
    if protocol_info.crf_domains:
        # 將領域分組顯示
        domains_per_row = 3
        for i in range(0, len(protocol_info.crf_domains), domains_per_row):
            row_domains = protocol_info.crf_domains[i:i+domains_per_row]
            print("  " + " | ".join(f"{d:30}" for d in row_domains))
    else:
        print("  未提取到 CRF 領域")

    # ========== 保存結果 ==========
    print("\n" + "=" * 80)
    print("保存結果")
    print("=" * 80)

    # 生成輸出檔案名稱（基於 protocol number 或 PDF 檔名）
    if protocol_info.protocol_number:
        output_filename = f"{protocol_info.protocol_number}_info.json"
    else:
        output_filename = f"{Path(PDF_PATH).stem}_info.json"

    output_path = OUTPUT_DIR / output_filename

    try:
        parser.save_to_json(protocol_info, str(output_path))
        print(f"✓ JSON 檔案已保存: {output_path}")
        print(f"  檔案大小: {output_path.stat().st_size:,} bytes")
    except Exception as e:
        print(f"✗ 保存失敗: {e}")

    # 也可以保存為 Python dict
    python_output_path = OUTPUT_DIR / f"{Path(output_filename).stem}_dict.txt"
    try:
        with open(python_output_path, 'w', encoding='utf-8') as f:
            f.write("# Protocol Information Dictionary\n\n")
            f.write(str(protocol_info.to_dict()))
        print(f"✓ Python Dict 已保存: {python_output_path}")
    except Exception as e:
        print(f"✗ 保存 Python Dict 失敗: {e}")

    # ========== 資料品質檢查 ==========
    print("\n" + "=" * 80)
    print("資料品質檢查")
    print("=" * 80)

    fields = {
        "試驗標題": protocol_info.study_title,
        "Protocol 編號": protocol_info.protocol_number,
        "贊助商": protocol_info.sponsor,
        "試驗階段": protocol_info.phase,
        "試驗設計": protocol_info.study_design,
        "目標族群": protocol_info.target_population,
        "樣本數": protocol_info.sample_size,
        "訪視時程": protocol_info.visit_schedule,
        "主要終點": protocol_info.primary_endpoints,
        "次要終點": protocol_info.secondary_endpoints,
        "納入標準": protocol_info.inclusion_criteria,
        "排除標準": protocol_info.exclusion_criteria,
        "CRF 領域": protocol_info.crf_domains,
    }

    extracted_count = sum(1 for v in fields.values() if v)
    total_count = len(fields)
    completion_rate = (extracted_count / total_count) * 100

    print(f"\n提取完整度: {extracted_count}/{total_count} ({completion_rate:.1f}%)")
    print("\n欄位狀態:")
    for field_name, field_value in fields.items():
        status = "✓" if field_value else "✗"
        value_info = ""
        if isinstance(field_value, list):
            value_info = f"({len(field_value)} 項)"
        elif isinstance(field_value, str):
            value_info = f"({len(field_value)} 字元)"

        print(f"  {status} {field_name:15} {value_info}")

    print("\n" + "=" * 80)
    print("處理完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
