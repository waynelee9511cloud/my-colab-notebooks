"""
CRF Generator - Example Usage Script

This script demonstrates various ways to use the CRF Generator module.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.crf_generator import CRFGenerator, CRFDomain


def example_1_basic_crf():
    """Example 1: Generate a basic CRF with standard domains."""

    print("\n" + "="*80)
    print("Example 1: Basic CRF Generation")
    print("="*80 + "\n")

    # Define protocol information
    protocol_info = {
        'study_title': 'A Phase III Study of Novel Immunotherapy in Metastatic Melanoma',
        'protocol_number': 'ONCO-2025-123',
        'sponsor': 'Global Pharma Research',
        'version': '1.0'
    }

    # Create generator
    generator = CRFGenerator(protocol_info)

    # Generate CRF with all standard domains
    output_path = os.path.join('..', 'output', 'basic_CRF.docx')
    crf_file = generator.generate_crf(
        output_path=output_path,
        include_all_standard=True
    )

    print(f"✓ Generated CRF with all standard domains: {crf_file}")


def example_2_selected_domains():
    """Example 2: Generate CRF with selected domains only."""

    print("\n" + "="*80)
    print("Example 2: CRF with Selected Domains")
    print("="*80 + "\n")

    protocol_info = {
        'study_title': 'Safety Study of Drug Y in Healthy Volunteers',
        'protocol_number': 'SAFETY-2025-456',
        'sponsor': 'BioTech Solutions Inc.',
        'version': '2.0'
    }

    generator = CRFGenerator(protocol_info)

    # Generate CRF with only specific domains
    selected_domains = [
        'demographics',
        'vital_signs',
        'laboratory_tests',
        'adverse_events'
    ]

    output_path = os.path.join('..', 'output', 'selected_domains_CRF.docx')
    crf_file = generator.generate_crf(
        domains=selected_domains,
        output_path=output_path
    )

    print(f"✓ Generated CRF with {len(selected_domains)} selected domains: {crf_file}")


def example_3_custom_domain():
    """Example 3: Add custom domains to CRF."""

    print("\n" + "="*80)
    print("Example 3: CRF with Custom Domains")
    print("="*80 + "\n")

    protocol_info = {
        'study_title': 'Cardiac Function Study in Heart Failure Patients',
        'protocol_number': 'CARDIO-2025-789',
        'sponsor': 'Cardiovascular Research Center',
        'version': '1.0'
    }

    generator = CRFGenerator(protocol_info)

    # Define custom Echocardiography domain
    echo_domain = CRFDomain(
        name='Echocardiography',
        description='Cardiac ultrasound assessment',
        fields=[
            {
                'name': 'assessment_date',
                'label': 'Assessment Date',
                'type': 'date',
                'required': True,
                'coding_instruction': 'Date of echocardiogram'
            },
            {
                'name': 'ejection_fraction',
                'label': 'Left Ventricular Ejection Fraction (LVEF)',
                'type': 'numeric',
                'required': True,
                'unit': '%',
                'coding_instruction': 'LVEF percentage calculated by biplane Simpson method'
            },
            {
                'name': 'lvedd',
                'label': 'Left Ventricular End-Diastolic Dimension',
                'type': 'numeric',
                'required': True,
                'unit': 'mm',
                'coding_instruction': 'LVEDD measurement in millimeters'
            },
            {
                'name': 'lvesd',
                'label': 'Left Ventricular End-Systolic Dimension',
                'type': 'numeric',
                'required': True,
                'unit': 'mm',
                'coding_instruction': 'LVESD measurement in millimeters'
            },
            {
                'name': 'wall_motion',
                'label': 'Wall Motion Abnormality',
                'type': 'dropdown',
                'required': True,
                'options': ['None', 'Hypokinesis', 'Akinesis', 'Dyskinesis'],
                'coding_instruction': 'Assessment of regional wall motion abnormalities'
            },
            {
                'name': 'valve_function',
                'label': 'Valve Function',
                'type': 'dropdown',
                'required': True,
                'options': ['Normal', 'Mild Regurgitation', 'Moderate Regurgitation', 'Severe Regurgitation', 'Stenosis'],
                'coding_instruction': 'Overall valve function assessment'
            }
        ]
    )

    # Define custom ECG domain
    ecg_domain = CRFDomain(
        name='Electrocardiogram (ECG)',
        description='12-lead ECG assessment',
        fields=[
            {
                'name': 'assessment_date',
                'label': 'ECG Date',
                'type': 'date',
                'required': True,
                'coding_instruction': 'Date ECG was performed'
            },
            {
                'name': 'assessment_time',
                'label': 'ECG Time',
                'type': 'text',
                'required': True,
                'coding_instruction': 'Time ECG was performed (24-hour format)'
            },
            {
                'name': 'heart_rate',
                'label': 'Heart Rate',
                'type': 'numeric',
                'required': True,
                'unit': 'bpm',
                'coding_instruction': 'Heart rate from ECG in beats per minute'
            },
            {
                'name': 'pr_interval',
                'label': 'PR Interval',
                'type': 'numeric',
                'required': True,
                'unit': 'ms',
                'coding_instruction': 'PR interval in milliseconds'
            },
            {
                'name': 'qrs_duration',
                'label': 'QRS Duration',
                'type': 'numeric',
                'required': True,
                'unit': 'ms',
                'coding_instruction': 'QRS complex duration in milliseconds'
            },
            {
                'name': 'qt_interval',
                'label': 'QT Interval',
                'type': 'numeric',
                'required': True,
                'unit': 'ms',
                'coding_instruction': 'QT interval in milliseconds'
            },
            {
                'name': 'qtc_interval',
                'label': 'QTc Interval (Corrected)',
                'type': 'numeric',
                'required': True,
                'unit': 'ms',
                'coding_instruction': 'QTc interval using Fridericia correction formula'
            },
            {
                'name': 'rhythm',
                'label': 'Rhythm',
                'type': 'dropdown',
                'required': True,
                'options': ['Sinus Rhythm', 'Atrial Fibrillation', 'Atrial Flutter', 'Other Arrhythmia'],
                'coding_instruction': 'Overall cardiac rhythm'
            },
            {
                'name': 'clinically_significant',
                'label': 'Clinically Significant Findings',
                'type': 'dropdown',
                'required': True,
                'options': ['Yes', 'No'],
                'coding_instruction': 'Investigator assessment of clinical significance'
            }
        ]
    )

    # Add custom domains
    generator.add_custom_domain(echo_domain)
    generator.add_custom_domain(ecg_domain)

    # Generate CRF with standard and custom domains
    domains_to_include = [
        'demographics',
        'vital_signs',
        'echocardiography',
        'electrocardiogram_(ecg)',
        'adverse_events'
    ]

    output_path = os.path.join('..', 'output', 'cardiac_study_CRF.docx')
    crf_file = generator.generate_crf(
        domains=domains_to_include,
        output_path=output_path
    )

    print(f"✓ Generated CRF with custom cardiac domains: {crf_file}")


def example_4_oncology_study():
    """Example 4: Comprehensive oncology study CRF."""

    print("\n" + "="*80)
    print("Example 4: Oncology Study CRF")
    print("="*80 + "\n")

    protocol_info = {
        'study_title': 'A Multicenter Study of Targeted Therapy in Non-Small Cell Lung Cancer',
        'protocol_number': 'LUNG-2025-999',
        'sponsor': 'Oncology Research Consortium',
        'version': '3.0'
    }

    generator = CRFGenerator(protocol_info)

    # Define tumor assessment domain
    tumor_domain = CRFDomain(
        name='Tumor Assessment',
        description='RECIST 1.1 tumor response evaluation',
        fields=[
            {
                'name': 'assessment_date',
                'label': 'Assessment Date',
                'type': 'date',
                'required': True,
                'coding_instruction': 'Date of imaging assessment'
            },
            {
                'name': 'imaging_modality',
                'label': 'Imaging Modality',
                'type': 'dropdown',
                'required': True,
                'options': ['CT Scan', 'MRI', 'PET-CT', 'Other'],
                'coding_instruction': 'Type of imaging used for assessment'
            },
            {
                'name': 'target_lesion_sum',
                'label': 'Sum of Target Lesions',
                'type': 'numeric',
                'required': True,
                'unit': 'mm',
                'coding_instruction': 'Sum of longest diameters of all target lesions'
            },
            {
                'name': 'new_lesions',
                'label': 'New Lesions',
                'type': 'dropdown',
                'required': True,
                'options': ['Yes', 'No'],
                'coding_instruction': 'Presence of any new lesions'
            },
            {
                'name': 'non_target_progression',
                'label': 'Non-Target Lesion Progression',
                'type': 'dropdown',
                'required': True,
                'options': ['Yes', 'No', 'Not Applicable'],
                'coding_instruction': 'Unequivocal progression of non-target lesions'
            },
            {
                'name': 'overall_response',
                'label': 'Overall Response',
                'type': 'dropdown',
                'required': True,
                'options': ['Complete Response (CR)', 'Partial Response (PR)', 'Stable Disease (SD)', 'Progressive Disease (PD)', 'Not Evaluable'],
                'coding_instruction': 'Overall response per RECIST 1.1 criteria'
            }
        ]
    )

    # Define biomarker domain
    biomarker_domain = CRFDomain(
        name='Biomarker Analysis',
        description='Molecular biomarker testing results',
        fields=[
            {
                'name': 'sample_collection_date',
                'label': 'Sample Collection Date',
                'type': 'date',
                'required': True,
                'coding_instruction': 'Date tissue/blood sample was collected'
            },
            {
                'name': 'sample_type',
                'label': 'Sample Type',
                'type': 'dropdown',
                'required': True,
                'options': ['Tumor Tissue', 'Blood (Plasma)', 'Blood (Serum)', 'Other'],
                'coding_instruction': 'Type of biological sample'
            },
            {
                'name': 'egfr_mutation',
                'label': 'EGFR Mutation Status',
                'type': 'dropdown',
                'required': True,
                'options': ['Positive', 'Negative', 'Not Tested'],
                'coding_instruction': 'EGFR mutation presence'
            },
            {
                'name': 'alk_rearrangement',
                'label': 'ALK Rearrangement',
                'type': 'dropdown',
                'required': True,
                'options': ['Positive', 'Negative', 'Not Tested'],
                'coding_instruction': 'ALK gene rearrangement status'
            },
            {
                'name': 'pdl1_expression',
                'label': 'PD-L1 Expression',
                'type': 'text',
                'required': False,
                'unit': '%',
                'coding_instruction': 'PD-L1 tumor proportion score (TPS) percentage'
            }
        ]
    )

    # Add custom domains
    generator.add_custom_domain(tumor_domain)
    generator.add_custom_domain(biomarker_domain)

    # Generate comprehensive oncology CRF
    domains_to_include = [
        'demographics',
        'medical_history',
        'vital_signs',
        'laboratory_tests',
        'tumor_assessment',
        'biomarker_analysis',
        'study_drug_administration',
        'adverse_events',
        'concomitant_medications'
    ]

    output_path = os.path.join('..', 'output', 'oncology_study_CRF.docx')
    crf_file = generator.generate_crf(
        domains=domains_to_include,
        output_path=output_path
    )

    print(f"✓ Generated comprehensive oncology CRF: {crf_file}")


def example_5_export_domain_template():
    """Example 5: Export individual domain as template."""

    print("\n" + "="*80)
    print("Example 5: Export Domain Template")
    print("="*80 + "\n")

    generator = CRFGenerator()

    # Export specific domains as templates
    domains_to_export = ['adverse_events', 'vital_signs', 'laboratory_tests']

    for domain in domains_to_export:
        output_path = os.path.join('..', 'output', f'{domain}_template.docx')
        generator.export_domain_template(domain, output_path)
        print(f"✓ Exported {domain} template")


def example_6_list_available_domains():
    """Example 6: List all available domains."""

    print("\n" + "="*80)
    print("Example 6: List Available Domains")
    print("="*80 + "\n")

    generator = CRFGenerator()

    print("Standard Domains:")
    print("-" * 40)
    for i, domain in enumerate(generator.STANDARD_DOMAINS.keys(), 1):
        domain_info = generator.STANDARD_DOMAINS[domain]
        print(f"{i}. {domain_info['name']}")
        print(f"   Description: {domain_info['description']}")
        print(f"   Fields: {len(domain_info['fields'])}")
        print()


def main():
    """Run all examples."""

    print("\n" + "="*80)
    print("CRF Generator - Demonstration Examples")
    print("="*80)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Run examples
    try:
        example_1_basic_crf()
        example_2_selected_domains()
        example_3_custom_domain()
        example_4_oncology_study()
        example_5_export_domain_template()
        example_6_list_available_domains()

        print("\n" + "="*80)
        print("All examples completed successfully!")
        print(f"Check the '{output_dir}' directory for generated CRF files.")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
