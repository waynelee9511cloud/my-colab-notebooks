#!/usr/bin/env python3
"""
Clinical Document Automation - 使用範例

這個檔案展示了如何使用 ClinicalDocAutomation 類別來自動生成所有臨床試驗文件。

Author: Clinical Documentation Automation Team
Date: 2025-11-18
"""

import os
import sys
from pathlib import Path

# 添加父目錄到路徑以便導入模組
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation_workflow import ClinicalDocAutomation, BatchProcessor


def example_1_basic_usage():
    """
    範例 1: 基本使用 - 生成所有文件

    這是最簡單的使用方式，會自動生成所有類型的文件。
    """
    print("=" * 80)
    print("範例 1: 基本使用 - 生成所有文件")
    print("=" * 80)

    # 設置參數
    protocol_pdf = "path/to/your/protocol.pdf"  # 替換為實際的 PDF 路徑
    api_key = "YOUR_GEMINI_API_KEY"  # 替換為您的 API Key

    # 或者從環境變數讀取
    # api_key = os.getenv("GEMINI_API_KEY")

    # 創建自動化實例
    automation = ClinicalDocAutomation(
        protocol_pdf=protocol_pdf,
        api_key=api_key,
        verbose=True  # 顯示詳細日誌
    )

    # 執行所有文件生成
    report = automation.run_all()

    # 顯示結果
    print("\n執行結果:")
    print(f"完成任務: {report.completed_tasks}/{report.total_tasks}")
    print(f"生成檔案數: {len(report.generated_files)}")

    for file_path in report.generated_files:
        print(f"  - {file_path}")


def example_2_selective_generation():
    """
    範例 2: 選擇性生成 - 只生成特定文件

    如果您只需要生成某些類型的文件，可以指定 generate_types 參數。
    """
    print("\n" + "=" * 80)
    print("範例 2: 選擇性生成 - 只生成 CRF 和 DVP")
    print("=" * 80)

    protocol_pdf = "path/to/your/protocol.pdf"
    api_key = "YOUR_GEMINI_API_KEY"

    automation = ClinicalDocAutomation(
        protocol_pdf=protocol_pdf,
        api_key=api_key,
        output_dir="output_selective",  # 自訂輸出目錄
        verbose=False
    )

    # 只生成 CRF 和 DVP
    report = automation.run_all(generate_types=['crf', 'dvp'])

    print(f"\n生成的文件: {len(report.generated_files)}")


def example_3_custom_output_directory():
    """
    範例 3: 自訂輸出目錄

    您可以指定自己的輸出目錄結構。
    """
    print("\n" + "=" * 80)
    print("範例 3: 自訂輸出目錄")
    print("=" * 80)

    protocol_pdf = "path/to/your/protocol.pdf"
    api_key = "YOUR_GEMINI_API_KEY"

    # 創建專案特定的輸出目錄
    project_name = "PROTO-2025-001"
    output_dir = f"projects/{project_name}/generated_docs"

    automation = ClinicalDocAutomation(
        protocol_pdf=protocol_pdf,
        api_key=api_key,
        output_dir=output_dir,
        verbose=True
    )

    report = automation.run_all()

    print(f"\n所有文件已保存至: {output_dir}")


def example_4_batch_processing():
    """
    範例 4: 批次處理 - 一次處理多個 Protocol

    當您有多個 Protocol 需要處理時，可以使用 BatchProcessor。
    """
    print("\n" + "=" * 80)
    print("範例 4: 批次處理")
    print("=" * 80)

    # 多個 Protocol PDF 檔案
    protocol_pdfs = [
        "protocols/protocol_001.pdf",
        "protocols/protocol_002.pdf",
        "protocols/protocol_003.pdf",
    ]

    api_key = "YOUR_GEMINI_API_KEY"

    # 創建批次處理器
    processor = BatchProcessor(
        api_key=api_key,
        output_base_dir="batch_output",
        verbose=True
    )

    # 批次處理所有 Protocol
    results = processor.process_protocols(
        protocol_pdfs=protocol_pdfs,
        generate_types=['crf', 'dvp', 'user_guide']  # 可選：指定要生成的文件類型
    )

    # 顯示結果摘要
    print(f"\n批次處理完成！")
    print(f"處理的 Protocol 數量: {len(results)}")

    for protocol_path, report in results:
        print(f"\n{Path(protocol_path).name}:")
        print(f"  完成: {report.completed_tasks}")
        print(f"  失敗: {report.failed_tasks}")


def example_5_error_handling():
    """
    範例 5: 錯誤處理和報告

    展示如何處理錯誤和檢查執行報告。
    """
    print("\n" + "=" * 80)
    print("範例 5: 錯誤處理")
    print("=" * 80)

    protocol_pdf = "path/to/your/protocol.pdf"
    api_key = "YOUR_GEMINI_API_KEY"

    try:
        automation = ClinicalDocAutomation(
            protocol_pdf=protocol_pdf,
            api_key=api_key,
            verbose=True,
            backup=True  # 啟用備份功能
        )

        report = automation.run_all()

        # 檢查是否有錯誤
        if report.failed_tasks > 0:
            print("\n警告: 有任務執行失敗！")
            print("失敗的任務:")
            for task in report.tasks:
                if task.status == 'failed':
                    print(f"  - {task.task_type}: {task.error_message}")

        # 檢查是否有跳過的任務
        if report.skipped_tasks > 0:
            print("\n資訊: 有任務被跳過")
            for task in report.tasks:
                if task.status == 'skipped':
                    print(f"  - {task.task_type}: {task.error_message}")

        # 保存詳細報告
        print(f"\n詳細報告已保存至: {automation.output_dir}")

    except FileNotFoundError as e:
        print(f"錯誤: {e}")
        print("請確認 Protocol PDF 檔案路徑正確")
    except ValueError as e:
        print(f"錯誤: {e}")
        print("請檢查 API Key 是否正確")
    except Exception as e:
        print(f"未預期的錯誤: {e}")
        import traceback
        traceback.print_exc()


def example_6_working_with_report():
    """
    範例 6: 使用執行報告

    展示如何使用和分析執行報告。
    """
    print("\n" + "=" * 80)
    print("範例 6: 使用執行報告")
    print("=" * 80)

    protocol_pdf = "path/to/your/protocol.pdf"
    api_key = "YOUR_GEMINI_API_KEY"

    automation = ClinicalDocAutomation(
        protocol_pdf=protocol_pdf,
        api_key=api_key
    )

    report = automation.run_all()

    # 1. 獲取 Protocol 資訊
    if report.protocol_info:
        print("\nProtocol 資訊:")
        print(f"  標題: {report.protocol_info.get('study_title')}")
        print(f"  編號: {report.protocol_info.get('protocol_number')}")
        print(f"  階段: {report.protocol_info.get('phase')}")

    # 2. 列出所有生成的檔案
    print("\n生成的檔案:")
    for file_path in report.generated_files:
        file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
        print(f"  - {Path(file_path).name} ({file_size:,} bytes)")

    # 3. 任務執行時間分析
    print("\n任務執行時間:")
    for task in report.tasks:
        if task.start_time and task.end_time:
            from datetime import datetime
            start = datetime.fromisoformat(task.start_time)
            end = datetime.fromisoformat(task.end_time)
            duration = (end - start).total_seconds()
            print(f"  - {task.task_type}: {duration:.2f} 秒")

    # 4. 保存報告為 JSON
    json_report_path = automation.output_dir / "my_custom_report.json"
    report.save_to_file(str(json_report_path))
    print(f"\n自訂報告已保存: {json_report_path}")

    # 5. 獲取 JSON 字符串（可用於 API 回傳等）
    json_string = report.to_json()
    print(f"\nJSON 報告長度: {len(json_string)} 字元")


def example_7_environment_variables():
    """
    範例 7: 使用環境變數

    展示如何使用環境變數來管理敏感資訊（如 API Key）。
    """
    print("\n" + "=" * 80)
    print("範例 7: 使用環境變數")
    print("=" * 80)

    # 從環境變數讀取 API Key（更安全的做法）
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("錯誤: 請設置環境變數 GEMINI_API_KEY")
        print("\n在 Linux/Mac 上:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        print("\n在 Windows 上:")
        print("  set GEMINI_API_KEY=your-api-key-here")
        return

    protocol_pdf = "path/to/your/protocol.pdf"

    automation = ClinicalDocAutomation(
        protocol_pdf=protocol_pdf,
        api_key=api_key,  # 從環境變數讀取
        verbose=True
    )

    report = automation.run_all()
    print(f"\n處理完成！API Key 安全地從環境變數讀取。")


def main():
    """
    主函數 - 運行所有範例

    注意: 實際使用時，請將 'path/to/your/protocol.pdf' 和 'YOUR_GEMINI_API_KEY'
          替換為真實的值，或註釋掉不需要的範例。
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "Clinical Document Automation - 使用範例".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    print("本檔案包含多個使用範例，展示不同的使用場景。")
    print("請根據您的需求參考相應的範例函數。")
    print("\n")

    # 列出所有範例
    examples = [
        ("example_1_basic_usage", "基本使用 - 生成所有文件"),
        ("example_2_selective_generation", "選擇性生成 - 只生成特定文件"),
        ("example_3_custom_output_directory", "自訂輸出目錄"),
        ("example_4_batch_processing", "批次處理 - 一次處理多個 Protocol"),
        ("example_5_error_handling", "錯誤處理和報告"),
        ("example_6_working_with_report", "使用執行報告"),
        ("example_7_environment_variables", "使用環境變數"),
    ]

    print("可用的範例:")
    for i, (func_name, description) in enumerate(examples, 1):
        print(f"  {i}. {description}")
        print(f"     函數: {func_name}()")

    print("\n")
    print("要運行特定範例，請取消註釋相應的函數調用，並設置正確的參數。")
    print("\n")

    # 取消註釋以下行來運行特定範例：
    # example_1_basic_usage()
    # example_2_selective_generation()
    # example_3_custom_output_directory()
    # example_4_batch_processing()
    # example_5_error_handling()
    # example_6_working_with_report()
    # example_7_environment_variables()


if __name__ == "__main__":
    main()
