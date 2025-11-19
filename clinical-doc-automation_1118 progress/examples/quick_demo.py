"""
Quick Demo - Generate a sample DVP document
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.dvp_generator import (
    DVPGenerator,
    ProtocolInfo,
    CRFField,
    Severity,
    ValidationType
)


def main():
    print("=" * 80)
    print("DVP Generator - Quick Demo")
    print("=" * 80)

    # 定義試驗書資訊
    protocol_info = ProtocolInfo(
        protocol_number="DEMO-2025-001",
        protocol_title="A Phase III Study of Antihypertensive Drug in Essential Hypertension",
        sponsor="Demo Pharmaceuticals Inc.",
        indication="Essential Hypertension",
        phase="Phase III",
        version="1.0"
    )

    # 定義 CRF 欄位
    crf_fields = [
        # Demographics Form
        CRFField(
            field_name="subject_id",
            field_label="Subject ID",
            form_name="Demographics",
            data_type="text",
            required=True
        ),
        CRFField(
            field_name="age",
            field_label="Age",
            form_name="Demographics",
            data_type="numeric",
            required=True,
            min_value=18,
            max_value=75,
            units="years"
        ),
        CRFField(
            field_name="weight",
            field_label="Weight",
            form_name="Demographics",
            data_type="numeric",
            required=True,
            min_value=40,
            max_value=150,
            units="kg"
        ),
        CRFField(
            field_name="height",
            field_label="Height",
            form_name="Demographics",
            data_type="numeric",
            required=True,
            min_value=140,
            max_value=210,
            units="cm"
        ),

        # Informed Consent Form
        CRFField(
            field_name="consent_date",
            field_label="Informed Consent Date",
            form_name="Informed Consent",
            data_type="date",
            required=True
        ),

        # Vital Signs Form
        CRFField(
            field_name="visit_date",
            field_label="Visit Date",
            form_name="Vital Signs",
            data_type="date",
            required=True
        ),
        CRFField(
            field_name="systolic_bp",
            field_label="Systolic Blood Pressure",
            form_name="Vital Signs",
            data_type="numeric",
            required=True,
            min_value=90,
            max_value=200,
            units="mmHg"
        ),
        CRFField(
            field_name="diastolic_bp",
            field_label="Diastolic Blood Pressure",
            form_name="Vital Signs",
            data_type="numeric",
            required=True,
            min_value=50,
            max_value=130,
            units="mmHg"
        ),
        CRFField(
            field_name="heart_rate",
            field_label="Heart Rate",
            form_name="Vital Signs",
            data_type="numeric",
            required=True,
            min_value=40,
            max_value=150,
            units="bpm"
        ),

        # Laboratory Form
        CRFField(
            field_name="lab_date",
            field_label="Laboratory Test Date",
            form_name="Laboratory",
            data_type="date",
            required=True
        ),
        CRFField(
            field_name="creatinine",
            field_label="Serum Creatinine",
            form_name="Laboratory",
            data_type="numeric",
            required=True,
            min_value=0.5,
            max_value=3.0,
            units="mg/dL"
        ),

        # Adverse Events Form
        CRFField(
            field_name="ae_occurred",
            field_label="Did Adverse Event Occur",
            form_name="Adverse Events",
            data_type="dropdown",
            required=True,
            valid_values=["Yes", "No"]
        ),
        CRFField(
            field_name="ae_start_date",
            field_label="AE Start Date",
            form_name="Adverse Events",
            data_type="date"
        ),
        CRFField(
            field_name="ae_end_date",
            field_label="AE End Date",
            form_name="Adverse Events",
            data_type="date"
        ),
    ]

    print(f"\n1. 建立 DVP Generator (試驗書: {protocol_info.protocol_number})")
    generator = DVPGenerator(protocol_info)

    print(f"2. 新增 {len(crf_fields)} 個 CRF 欄位定義")
    generator.add_crf_fields(crf_fields)

    print("3. 生成標準驗證規則...")
    rules = generator.generate_all_rules()
    print(f"   - 共生成 {len(rules)} 個驗證規則")

    print("\n4. 新增自訂驗證規則...")
    # 自訂規則 1: BP 收案標準
    generator.add_custom_rule(
        description="Verify systolic BP ≥140 mmHg or diastolic BP ≥90 mmHg at screening (inclusion criteria)",
        query_text="Please verify blood pressure meets inclusion criteria (SBP ≥140 or DBP ≥90 mmHg).",
        severity=Severity.CRITICAL,
        validation_type=ValidationType.PROTOCOL_DEVIATION,
        form_name="Vital Signs"
    )

    # 自訂規則 2: 腎功能排除標準
    generator.add_custom_rule(
        description="Verify creatinine is within acceptable range per protocol (exclusion criteria)",
        query_text="Please verify creatinine level. Subjects with creatinine >2.5 mg/dL should be excluded.",
        severity=Severity.CRITICAL,
        validation_type=ValidationType.PROTOCOL_DEVIATION,
        form_name="Laboratory",
        field_name="creatinine"
    )

    print(f"   - 共新增 2 個自訂規則")
    print(f"   - 總規則數: {len(generator.validation_rules)}")

    print("\n5. 驗證規則摘要:")
    summary = generator.get_rules_summary()
    for rule_type, count in sorted(summary.items()):
        print(f"   - {rule_type}: {count}")

    # 建立輸出目錄
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)

    # 生成 DVP 文件
    output_path = os.path.join(output_dir, "demo_dvp.docx")
    print(f"\n6. 生成 DVP Word 文件...")
    doc_path = generator.generate_dvp_document(output_path)
    print(f"   ✓ DVP 文件已生成: {os.path.abspath(doc_path)}")

    # 匯出 JSON
    json_path = os.path.join(output_dir, "demo_dvp_rules.json")
    rules_dict = generator.export_rules_to_dict()

    import json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rules_dict, f, indent=2, ensure_ascii=False)
    print(f"   ✓ 驗證規則 JSON 已匯出: {os.path.abspath(json_path)}")

    print("\n" + "=" * 80)
    print("Demo 完成!")
    print("=" * 80)
    print(f"\n生成的檔案:")
    print(f"  1. Word 文件: {os.path.abspath(doc_path)}")
    print(f"  2. JSON 規則: {os.path.abspath(json_path)}")
    print(f"\n總共生成 {len(generator.validation_rules)} 個驗證規則")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
