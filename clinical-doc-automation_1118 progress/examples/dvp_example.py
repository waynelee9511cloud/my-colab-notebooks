"""
DVP Generator Usage Example

This example demonstrates how to use the DVP Generator module to create
a comprehensive Data Validation Plan for a clinical trial.
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
    ValidationType,
    create_dvp
)


def example_basic_usage():
    """Example 1: Basic usage with minimal setup"""
    print("=" * 80)
    print("Example 1: Basic DVP Generation")
    print("=" * 80)

    # Define protocol information
    protocol_info = ProtocolInfo(
        protocol_number="ABC-2025-001",
        protocol_title="A Phase III Study of Drug X in Patients with Disease Y",
        sponsor="ABC Pharmaceuticals",
        indication="Disease Y",
        phase="Phase III",
        version="1.0"
    )

    # Define CRF fields
    crf_fields = [
        # Demographics form
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
            max_value=85,
            units="years"
        ),
        CRFField(
            field_name="weight",
            field_label="Weight",
            form_name="Demographics",
            data_type="numeric",
            required=True,
            min_value=30,
            max_value=200,
            units="kg"
        ),
        CRFField(
            field_name="height",
            field_label="Height",
            form_name="Demographics",
            data_type="numeric",
            required=True,
            min_value=100,
            max_value=250,
            units="cm"
        ),

        # Informed Consent form
        CRFField(
            field_name="consent_date",
            field_label="Informed Consent Date",
            form_name="Informed Consent",
            data_type="date",
            required=True,
            date_format="YYYY-MM-DD"
        ),

        # Vital Signs form
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
            min_value=70,
            max_value=200,
            units="mmHg"
        ),
        CRFField(
            field_name="diastolic_bp",
            field_label="Diastolic Blood Pressure",
            form_name="Vital Signs",
            data_type="numeric",
            required=True,
            min_value=40,
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

        # Adverse Events form
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
            data_type="date",
            required=False
        ),
        CRFField(
            field_name="ae_end_date",
            field_label="AE End Date",
            form_name="Adverse Events",
            data_type="date",
            required=False
        ),
    ]

    # Create DVP generator
    generator = DVPGenerator(protocol_info)
    generator.add_crf_fields(crf_fields)

    # Generate all standard rules
    rules = generator.generate_all_rules()

    print(f"\nGenerated {len(rules)} validation rules")
    print("\nRules Summary:")
    summary = generator.get_rules_summary()
    for rule_type, count in sorted(summary.items()):
        print(f"  - {rule_type}: {count}")

    # Generate DVP document
    output_path = "../output/dvp_basic_example.docx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc_path = generator.generate_dvp_document(output_path)
    print(f"\nDVP document generated: {doc_path}")

    return generator


def example_with_custom_rules():
    """Example 2: Adding custom validation rules"""
    print("\n" + "=" * 80)
    print("Example 2: DVP with Custom Rules")
    print("=" * 80)

    # Define protocol information
    protocol_info = ProtocolInfo(
        protocol_number="XYZ-2025-002",
        protocol_title="A Study of Combination Therapy in Advanced Cancer",
        sponsor="XYZ Biotech",
        indication="Advanced Cancer",
        phase="Phase II",
        version="2.0"
    )

    # Define CRF fields
    crf_fields = [
        CRFField(
            field_name="tumor_size",
            field_label="Tumor Size",
            form_name="Tumor Assessment",
            data_type="numeric",
            required=True,
            min_value=0,
            max_value=500,
            units="mm"
        ),
        CRFField(
            field_name="ecog_status",
            field_label="ECOG Performance Status",
            form_name="Demographics",
            data_type="dropdown",
            required=True,
            valid_values=["0", "1", "2", "3", "4"]
        ),
    ]

    # Create DVP generator
    generator = DVPGenerator(protocol_info)
    generator.add_crf_fields(crf_fields)
    generator.generate_all_rules()

    # Add custom rules
    print("\nAdding custom validation rules...")

    # Custom rule 1: ECOG status protocol requirement
    generator.add_custom_rule(
        description="Verify that ECOG Performance Status is 0-2 per protocol inclusion criteria",
        query_text="Please verify ECOG Performance Status. Protocol requires ECOG 0-2 for enrollment.",
        severity=Severity.CRITICAL,
        validation_type=ValidationType.PROTOCOL_DEVIATION,
        form_name="Demographics",
        field_name="ecog_status",
        details={'allowed_values': ['0', '1', '2']}
    )

    # Custom rule 2: Tumor measurement consistency
    generator.add_custom_rule(
        description="Check that tumor size measurements are consistent with RECIST criteria",
        query_text="Please verify tumor measurements comply with RECIST 1.1 criteria.",
        severity=Severity.MAJOR,
        validation_type=ValidationType.LOGICAL_CHECK,
        form_name="Tumor Assessment",
        field_name="tumor_size",
        details={'criteria': 'RECIST 1.1'}
    )

    # Custom rule 3: Prior therapy requirement
    generator.add_custom_rule(
        description="Verify patient has received at least one prior line of therapy",
        query_text="Please confirm prior therapy. Protocol requires at least one prior line of treatment.",
        severity=Severity.CRITICAL,
        validation_type=ValidationType.PROTOCOL_DEVIATION,
        details={'requirement': 'minimum_1_prior_therapy'}
    )

    print(f"Total rules: {len(generator.validation_rules)}")

    # Generate document
    output_path = "../output/dvp_custom_example.docx"
    doc_path = generator.generate_dvp_document(output_path)
    print(f"\nDVP document generated: {doc_path}")

    return generator


def example_convenience_function():
    """Example 3: Using the convenience function"""
    print("\n" + "=" * 80)
    print("Example 3: Using Convenience Function")
    print("=" * 80)

    protocol_info = ProtocolInfo(
        protocol_number="DEF-2025-003",
        protocol_title="Pediatric Study of Safety and Efficacy",
        sponsor="DEF Research",
        indication="Pediatric Disease",
        phase="Phase I/II"
    )

    crf_fields = [
        CRFField(
            field_name="age",
            field_label="Age",
            form_name="Demographics",
            data_type="numeric",
            required=True,
            min_value=2,
            max_value=17,
            units="years"
        ),
        CRFField(
            field_name="parent_consent_date",
            field_label="Parental Consent Date",
            form_name="Informed Consent",
            data_type="date",
            required=True
        ),
    ]

    # Custom rules as dictionary
    custom_rules = [
        {
            'description': 'Verify parental consent is obtained for all subjects under 18',
            'query_text': 'Please confirm parental consent was obtained.',
            'severity': 'CRITICAL',
            'validation_type': 'PROTOCOL_DEVIATION',
            'form_name': 'Informed Consent',
            'details': {'requirement': 'parental_consent_required'}
        },
        {
            'description': 'Check that age is appropriate for pediatric study',
            'query_text': 'Please verify subject age. Study is for pediatric patients (2-17 years).',
            'severity': 'CRITICAL',
            'validation_type': 'PROTOCOL_DEVIATION',
            'form_name': 'Demographics',
            'field_name': 'age'
        }
    ]

    # Generate DVP using convenience function
    output_path = "../output/dvp_convenience_example.docx"
    doc_path = create_dvp(
        protocol_info=protocol_info,
        crf_fields=crf_fields,
        output_path=output_path,
        custom_rules=custom_rules
    )

    print(f"DVP document generated: {doc_path}")


def example_export_rules():
    """Example 4: Exporting rules to JSON format"""
    print("\n" + "=" * 80)
    print("Example 4: Exporting Rules to Dictionary/JSON")
    print("=" * 80)

    protocol_info = ProtocolInfo(
        protocol_number="GHI-2025-004",
        protocol_title="Biomarker Study",
        sponsor="GHI Labs",
        indication="Oncology",
        phase="Phase II"
    )

    crf_fields = [
        CRFField(
            field_name="biomarker_level",
            field_label="Biomarker Level",
            form_name="Laboratory",
            data_type="numeric",
            required=True,
            min_value=0,
            max_value=1000,
            units="ng/mL"
        ),
    ]

    generator = DVPGenerator(protocol_info)
    generator.add_crf_fields(crf_fields)
    generator.generate_all_rules()

    # Export to dictionary
    rules_dict = generator.export_rules_to_dict()

    print(f"\nExported {len(rules_dict)} rules to dictionary format")
    print("\nFirst rule example:")
    if rules_dict:
        import json
        print(json.dumps(rules_dict[0], indent=2))

    # This can be saved to JSON file
    import json
    json_path = "../output/validation_rules.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    with open(json_path, 'w') as f:
        json.dump(rules_dict, f, indent=2)

    print(f"\nRules exported to JSON: {json_path}")


def example_comprehensive_study():
    """Example 5: Comprehensive real-world scenario"""
    print("\n" + "=" * 80)
    print("Example 5: Comprehensive Real-World DVP")
    print("=" * 80)

    protocol_info = ProtocolInfo(
        protocol_number="COMP-2025-001",
        protocol_title="A Randomized, Double-Blind, Placebo-Controlled Study of Drug ABC in Hypertension",
        sponsor="Global Pharma Inc.",
        indication="Essential Hypertension",
        phase="Phase III",
        version="3.0"
    )

    # Comprehensive CRF definition
    crf_fields = []

    # Demographics
    demographics_fields = [
        ('subject_id', 'Subject ID', 'text', True, None, None),
        ('site_id', 'Site ID', 'text', True, None, None),
        ('age', 'Age', 'numeric', True, 18, 75, 'years'),
        ('gender', 'Gender', 'dropdown', True, None, None),
        ('race', 'Race', 'dropdown', True, None, None),
        ('ethnicity', 'Ethnicity', 'dropdown', True, None, None),
        ('weight', 'Weight', 'numeric', True, 40, 200, 'kg'),
        ('height', 'Height', 'numeric', True, 140, 220, 'cm'),
    ]

    for field_name, label, dtype, req, min_v, max_v, *units in demographics_fields:
        crf_fields.append(CRFField(
            field_name=field_name,
            field_label=label,
            form_name='Demographics',
            data_type=dtype,
            required=req,
            min_value=min_v,
            max_value=max_v,
            units=units[0] if units else None
        ))

    # Vital Signs (multiple visits)
    vital_fields = [
        ('visit_date', 'Visit Date', 'date', True, None, None),
        ('systolic_bp', 'Systolic BP', 'numeric', True, 90, 200, 'mmHg'),
        ('diastolic_bp', 'Diastolic BP', 'numeric', True, 50, 130, 'mmHg'),
        ('heart_rate', 'Heart Rate', 'numeric', True, 40, 150, 'bpm'),
        ('temperature', 'Temperature', 'numeric', True, 35.0, 40.0, '°C'),
    ]

    for field_name, label, dtype, req, min_v, max_v, *units in vital_fields:
        crf_fields.append(CRFField(
            field_name=field_name,
            field_label=label,
            form_name='Vital Signs',
            data_type=dtype,
            required=req,
            min_value=min_v,
            max_value=max_v,
            units=units[0] if units else None
        ))

    # Laboratory Tests
    lab_fields = [
        ('lab_date', 'Laboratory Date', 'date', True, None, None),
        ('hemoglobin', 'Hemoglobin', 'numeric', True, 8.0, 20.0, 'g/dL'),
        ('wbc', 'White Blood Cell Count', 'numeric', True, 2.0, 20.0, '10^9/L'),
        ('creatinine', 'Serum Creatinine', 'numeric', True, 0.5, 5.0, 'mg/dL'),
        ('alt', 'ALT', 'numeric', True, 5, 500, 'U/L'),
        ('ast', 'AST', 'numeric', True, 5, 500, 'U/L'),
    ]

    for field_name, label, dtype, req, min_v, max_v, *units in lab_fields:
        crf_fields.append(CRFField(
            field_name=field_name,
            field_label=label,
            form_name='Laboratory',
            data_type=dtype,
            required=req,
            min_value=min_v,
            max_value=max_v,
            units=units[0] if units else None
        ))

    # Adverse Events
    ae_fields = [
        ('ae_occurred', 'AE Occurred', 'dropdown', True, None, None),
        ('ae_term', 'AE Term', 'text', False, None, None),
        ('ae_start_date', 'AE Start Date', 'date', False, None, None),
        ('ae_end_date', 'AE End Date', 'date', False, None, None),
        ('ae_severity', 'AE Severity', 'dropdown', False, None, None),
        ('ae_serious', 'Serious AE', 'dropdown', False, None, None),
    ]

    for field_name, label, dtype, req, min_v, max_v in ae_fields:
        crf_fields.append(CRFField(
            field_name=field_name,
            field_label=label,
            form_name='Adverse Events',
            data_type=dtype,
            required=req,
            min_value=min_v,
            max_value=max_v
        ))

    # Concomitant Medications
    cm_fields = [
        ('cm_name', 'Medication Name', 'text', False, None, None),
        ('cm_start_date', 'Medication Start Date', 'date', False, None, None),
        ('cm_end_date', 'Medication End Date', 'date', False, None, None),
        ('cm_indication', 'Indication', 'text', False, None, None),
    ]

    for field_name, label, dtype, req, min_v, max_v in cm_fields:
        crf_fields.append(CRFField(
            field_name=field_name,
            field_label=label,
            form_name='Concomitant Medications',
            data_type=dtype,
            required=req,
            min_value=min_v,
            max_value=max_v
        ))

    # Create generator
    generator = DVPGenerator(protocol_info)
    generator.add_crf_fields(crf_fields)
    generator.generate_all_rules()

    # Add comprehensive custom rules
    custom_rules = [
        # Protocol-specific inclusion criteria
        {
            'desc': 'Verify systolic BP ≥140 mmHg or diastolic BP ≥90 mmHg at screening (inclusion criteria)',
            'query': 'Please verify BP meets inclusion criteria (SBP ≥140 or DBP ≥90 mmHg).',
            'severity': Severity.CRITICAL,
            'type': ValidationType.PROTOCOL_DEVIATION,
            'form': 'Vital Signs'
        },
        # BMI calculation
        {
            'desc': 'Check that BMI is between 18.5 and 40 kg/m² per protocol',
            'query': 'Please verify BMI. Protocol requires BMI 18.5-40 kg/m².',
            'severity': Severity.MAJOR,
            'type': ValidationType.PROTOCOL_DEVIATION,
            'form': 'Demographics'
        },
        # Lab safety limits
        {
            'desc': 'Check that ALT/AST are <3x ULN per protocol safety criteria',
            'query': 'Please verify liver function tests. Values exceed protocol-specified limits.',
            'severity': Severity.CRITICAL,
            'type': ValidationType.PROTOCOL_DEVIATION,
            'form': 'Laboratory'
        },
        # Medication compliance
        {
            'desc': 'Verify prohibited medications are not taken during study',
            'query': 'Please verify concomitant medication is allowed per protocol.',
            'severity': Severity.MAJOR,
            'type': ValidationType.PROTOCOL_DEVIATION,
            'form': 'Concomitant Medications'
        },
    ]

    for rule in custom_rules:
        generator.add_custom_rule(
            description=rule['desc'],
            query_text=rule['query'],
            severity=rule['severity'],
            validation_type=rule['type'],
            form_name=rule.get('form')
        )

    print(f"\nTotal validation rules: {len(generator.validation_rules)}")
    print("\nRules breakdown:")
    for rule_type, count in sorted(generator.get_rules_summary().items()):
        print(f"  - {rule_type}: {count}")

    # Generate comprehensive DVP
    output_path = "../output/dvp_comprehensive.docx"
    doc_path = generator.generate_dvp_document(output_path)
    print(f"\nComprehensive DVP document generated: {doc_path}")

    # Also export to JSON
    rules_dict = generator.export_rules_to_dict()
    json_path = "../output/dvp_comprehensive_rules.json"
    import json
    with open(json_path, 'w') as f:
        json.dump(rules_dict, f, indent=2)
    print(f"Rules exported to JSON: {json_path}")

    return generator


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("DVP Generator - Usage Examples")
    print("=" * 80)

    # Run all examples
    try:
        example_basic_usage()
        example_with_custom_rules()
        example_convenience_function()
        example_export_rules()
        example_comprehensive_study()

        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80)
        print("\nGenerated files can be found in the 'output' directory:")
        print("  - dvp_basic_example.docx")
        print("  - dvp_custom_example.docx")
        print("  - dvp_convenience_example.docx")
        print("  - dvp_comprehensive.docx")
        print("  - validation_rules.json")
        print("  - dvp_comprehensive_rules.json")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
