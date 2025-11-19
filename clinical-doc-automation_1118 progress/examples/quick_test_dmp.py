"""
Quick Test - DMP Generator
快速测试 DMP 生成器的所有核心功能

Author: Clinical Doc Automation Team
Date: 2025-11-18
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.dmp_generator import (
    DMPGenerator,
    ProtocolInfo,
    CRFDomain,
    Milestone,
    ValidationCheck,
    create_dmp_with_defaults
)


def quick_test():
    """快速测试 DMP 生成器"""

    print("\n" + "=" * 80)
    print("DMP Generator - Quick Test")
    print("=" * 80)

    # 测试 1: 基本生成
    print("\n[Test 1] 基本 DMP 生成...")
    try:
        protocol_info = ProtocolInfo(
            protocol_number="QUICK-TEST-001",
            protocol_title="Quick Test Protocol for DMP Generator",
            sponsor="Test Pharma Inc.",
            indication="Hypertension",
            phase="Phase II",
            study_design="Randomized, Double-Blind, Placebo-Controlled",
            sample_size="200 subjects",
            study_duration="18 months",
            version="1.0"
        )

        generator = DMPGenerator(protocol_info)

        # 设置 EDC 系统
        generator.set_edc_system("Medidata Rave v2023")

        # 添加几个 CRF 领域
        test_domains = [
            CRFDomain(
                domain_name="Demographics",
                description="Subject demographic information",
                visit_schedule=["Screening"],
                is_critical=True,
                validation_rules=8
            ),
            CRFDomain(
                domain_name="Vital Signs",
                description="Blood pressure, heart rate, temperature",
                visit_schedule=["Screening", "Week 4", "Week 8", "Week 12"],
                is_critical=False,
                validation_rules=15
            ),
            CRFDomain(
                domain_name="Adverse Events",
                description="All adverse events",
                visit_schedule=["All visits"],
                is_critical=True,
                validation_rules=20
            )
        ]

        for domain in test_domains:
            generator.add_crf_domain(domain)

        # 添加几个里程碑
        test_milestones = [
            Milestone(
                name="Database Design",
                description="Complete database design and build",
                planned_date="15-Feb-2025",
                responsible="Clinical Data Manager"
            ),
            Milestone(
                name="First Subject In",
                description="First subject enrolled",
                planned_date="01-Mar-2025",
                responsible="Clinical Operations"
            ),
            Milestone(
                name="Database Lock",
                description="Lock clinical database",
                planned_date="31-Aug-2026",
                responsible="Data Management Lead"
            )
        ]

        for milestone in test_milestones:
            generator.add_milestone(milestone)

        # 添加自定义验证检查
        generator.add_validation_check(
            ValidationCheck(
                check_type="Blood Pressure Range Check",
                description="Verify systolic BP between 90-200 mmHg",
                severity="Major",
                implementation="Real-time"
            )
        )

        # 生成文档
        output_dir = "/tmp/dmp_quick_test"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "DMP_Quick_Test.docx")

        result = generator.generate_dmp_document(output_path, use_word_formatter=False)

        print(f"✓ DMP 文档已生成: {result}")
        print(f"  - Protocol: {protocol_info.protocol_number}")
        print(f"  - CRF Domains: {len(generator.crf_domains)}")
        print(f"  - Milestones: {len(generator.milestones)}")
        print(f"  - Validation Checks: {len(generator.validation_checks)}")
        print(f"  - File Size: {os.path.getsize(result):,} bytes")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # 测试 2: 快速创建函数
    print("\n[Test 2] 快速创建函数测试...")
    try:
        output_path = os.path.join(output_dir, "DMP_Quick_Create.docx")

        result = create_dmp_with_defaults(
            protocol_number="QUICK-CREATE-001",
            protocol_title="Quick Create Test",
            sponsor="Quick Pharma",
            indication="Diabetes",
            phase="Phase III",
            output_path=output_path
        )

        print(f"✓ 快速创建 DMP 成功: {result}")
        print(f"  - File Size: {os.path.getsize(result):,} bytes")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        return False

    # 测试 3: 导出配置
    print("\n[Test 3] 导出配置测试...")
    try:
        config_dict = generator.export_to_dict()

        print(f"✓ 配置导出成功")
        print(f"  - Protocol Info: {bool(config_dict['protocol_info'])}")
        print(f"  - DM Roles: {len(config_dict['dm_roles'])}")
        print(f"  - CRF Domains: {len(config_dict['crf_domains'])}")
        print(f"  - Validation Checks: {len(config_dict['validation_checks'])}")
        print(f"  - Milestones: {len(config_dict['milestones'])}")

    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        return False

    # 总结
    print("\n" + "=" * 80)
    print("Quick Test Summary")
    print("=" * 80)
    print("✓ All tests passed!")
    print(f"\n生成的文件保存在: {output_dir}/")
    print("  - DMP_Quick_Test.docx")
    print("  - DMP_Quick_Create.docx")
    print("\n可以使用 Microsoft Word 或 LibreOffice 打开这些文件。")
    print("=" * 80)

    return True


if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
