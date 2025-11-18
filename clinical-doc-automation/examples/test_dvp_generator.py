"""
Simple test script for DVP Generator module
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.dvp_generator import (
    DVPGenerator,
    ProtocolInfo,
    CRFField,
    ValidationRule,
    Severity,
    ValidationType
)


def test_protocol_info():
    """Test ProtocolInfo creation"""
    print("Testing ProtocolInfo...")

    protocol = ProtocolInfo(
        protocol_number="TEST-001",
        protocol_title="Test Study",
        sponsor="Test Sponsor",
        indication="Test Indication",
        phase="Phase I"
    )

    assert protocol.protocol_number == "TEST-001"
    assert protocol.protocol_title == "Test Study"
    assert protocol.version == "1.0"
    print("✓ ProtocolInfo test passed")


def test_crf_field():
    """Test CRFField creation"""
    print("Testing CRFField...")

    field = CRFField(
        field_name="age",
        field_label="Age",
        form_name="Demographics",
        data_type="numeric",
        required=True,
        min_value=18,
        max_value=65,
        units="years"
    )

    assert field.field_name == "age"
    assert field.required == True
    assert field.min_value == 18
    print("✓ CRFField test passed")


def test_validation_rule():
    """Test ValidationRule creation"""
    print("Testing ValidationRule...")

    rule = ValidationRule(
        rule_id="TEST-001",
        description="Test rule",
        severity=Severity.MAJOR,
        query_text="Test query",
        validation_type=ValidationType.RANGE_CHECK
    )

    assert rule.rule_id == "TEST-001"
    assert rule.severity == Severity.MAJOR
    assert rule.validation_type == ValidationType.RANGE_CHECK
    print("✓ ValidationRule test passed")


def test_dvp_generator_basic():
    """Test basic DVP generator functionality"""
    print("Testing DVPGenerator basic functionality...")

    protocol = ProtocolInfo(
        protocol_number="TEST-002",
        protocol_title="DVP Generator Test",
        sponsor="Test Sponsor",
        indication="Testing",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    # Add CRF fields
    fields = [
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
            max_value=65,
            units="years"
        )
    ]

    generator.add_crf_fields(fields)
    assert len(generator.crf_fields) == 2
    print("✓ CRF fields added successfully")


def test_range_check_generation():
    """Test range check rule generation"""
    print("Testing range check generation...")

    protocol = ProtocolInfo(
        protocol_number="TEST-003",
        protocol_title="Range Check Test",
        sponsor="Test",
        indication="Test",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    # Add numeric field with range
    generator.add_crf_fields([
        CRFField(
            field_name="weight",
            field_label="Weight",
            form_name="Vitals",
            data_type="numeric",
            min_value=40,
            max_value=200,
            units="kg"
        )
    ])

    rules = generator.generate_range_checks()

    assert len(rules) == 1
    assert rules[0].validation_type == ValidationType.RANGE_CHECK
    assert rules[0].severity == Severity.MAJOR
    assert "40" in rules[0].description
    assert "200" in rules[0].description
    print(f"✓ Generated {len(rules)} range check rule(s)")


def test_required_field_generation():
    """Test required field rule generation"""
    print("Testing required field generation...")

    protocol = ProtocolInfo(
        protocol_number="TEST-004",
        protocol_title="Required Field Test",
        sponsor="Test",
        indication="Test",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    # Add required field
    generator.add_crf_fields([
        CRFField(
            field_name="consent_date",
            field_label="Consent Date",
            form_name="Consent",
            data_type="date",
            required=True
        )
    ])

    rules = generator.generate_required_field_checks()

    assert len(rules) == 1
    assert rules[0].validation_type == ValidationType.REQUIRED_FIELD
    assert rules[0].severity == Severity.CRITICAL
    print(f"✓ Generated {len(rules)} required field rule(s)")


def test_custom_rule_addition():
    """Test adding custom rules"""
    print("Testing custom rule addition...")

    protocol = ProtocolInfo(
        protocol_number="TEST-005",
        protocol_title="Custom Rule Test",
        sponsor="Test",
        indication="Test",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    # Add custom rule
    rule = generator.add_custom_rule(
        description="Custom test rule",
        query_text="This is a custom query",
        severity=Severity.MAJOR,
        validation_type=ValidationType.CUSTOM,
        form_name="TestForm",
        field_name="test_field"
    )

    assert len(generator.validation_rules) == 1
    assert rule.validation_type == ValidationType.CUSTOM
    assert rule.form_name == "TestForm"
    print("✓ Custom rule added successfully")


def test_generate_all_rules():
    """Test generating all standard rules"""
    print("Testing generate_all_rules...")

    protocol = ProtocolInfo(
        protocol_number="TEST-006",
        protocol_title="All Rules Test",
        sponsor="Test",
        indication="Test",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    # Add diverse CRF fields
    generator.add_crf_fields([
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
            max_value=65
        ),
        CRFField(
            field_name="consent_date",
            field_label="Informed Consent Date",
            form_name="Consent",
            data_type="date",
            required=True
        ),
        CRFField(
            field_name="visit_date",
            field_label="Visit Date",
            form_name="Visit",
            data_type="date"
        )
    ])

    rules = generator.generate_all_rules()

    assert len(rules) > 0
    print(f"✓ Generated {len(rules)} total rules")

    # Check summary
    summary = generator.get_rules_summary()
    print(f"  Rules by type: {summary}")


def test_export_rules():
    """Test exporting rules to dictionary"""
    print("Testing rule export...")

    protocol = ProtocolInfo(
        protocol_number="TEST-007",
        protocol_title="Export Test",
        sponsor="Test",
        indication="Test",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    generator.add_crf_fields([
        CRFField(
            field_name="test_field",
            field_label="Test Field",
            form_name="TestForm",
            data_type="numeric",
            required=True,
            min_value=0,
            max_value=100
        )
    ])

    generator.generate_all_rules()
    rules_dict = generator.export_rules_to_dict()

    assert isinstance(rules_dict, list)
    assert len(rules_dict) > 0
    assert 'rule_id' in rules_dict[0]
    assert 'description' in rules_dict[0]
    assert 'severity' in rules_dict[0]
    print(f"✓ Exported {len(rules_dict)} rules to dictionary")


def test_rule_id_generation():
    """Test rule ID generation"""
    print("Testing rule ID generation...")

    protocol = ProtocolInfo(
        protocol_number="TEST-008",
        protocol_title="Rule ID Test",
        sponsor="Test",
        indication="Test",
        phase="Phase I"
    )

    generator = DVPGenerator(protocol)

    # Generate different types of rules
    id1 = generator._generate_rule_id(ValidationType.RANGE_CHECK)
    id2 = generator._generate_rule_id(ValidationType.REQUIRED_FIELD)
    id3 = generator._generate_rule_id(ValidationType.RANGE_CHECK)

    assert id1.startswith("RNG-")
    assert id2.startswith("REQ-")
    assert id3.startswith("RNG-")
    assert id1 != id3  # Should be unique
    print(f"✓ Rule IDs generated: {id1}, {id2}, {id3}")


def test_severity_levels():
    """Test severity level enumeration"""
    print("Testing severity levels...")

    assert Severity.CRITICAL.value == "Critical"
    assert Severity.MAJOR.value == "Major"
    assert Severity.MINOR.value == "Minor"
    print("✓ Severity levels verified")


def test_validation_types():
    """Test validation type enumeration"""
    print("Testing validation types...")

    types = [
        ValidationType.RANGE_CHECK,
        ValidationType.REQUIRED_FIELD,
        ValidationType.LOGICAL_CHECK,
        ValidationType.CROSS_FORM,
        ValidationType.DATE_CONSISTENCY,
        ValidationType.PROTOCOL_DEVIATION,
        ValidationType.CUSTOM
    ]

    assert len(types) == 7
    assert ValidationType.RANGE_CHECK.value == "Range Check"
    print(f"✓ {len(types)} validation types verified")


def run_all_tests():
    """Run all test functions"""
    print("\n" + "=" * 80)
    print("Running DVP Generator Tests")
    print("=" * 80 + "\n")

    tests = [
        test_protocol_info,
        test_crf_field,
        test_validation_rule,
        test_dvp_generator_basic,
        test_range_check_generation,
        test_required_field_generation,
        test_custom_rule_addition,
        test_generate_all_rules,
        test_export_rules,
        test_rule_id_generation,
        test_severity_levels,
        test_validation_types
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
            print()
        except AssertionError as e:
            print(f"✗ Test failed: {e}\n")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}\n")
            failed += 1

    print("=" * 80)
    print(f"Test Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 80)

    if failed == 0:
        print("\n✓ All tests passed!")
        return True
    else:
        print(f"\n✗ {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
