"""
Example: EDC/ePRO User Guide Generation

This example demonstrates how to use the UserGuideGenerator module to create
comprehensive user guides for EDC/ePRO systems.

Author: Clinical Documentation Automation Team
Date: 2025-11-18
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.user_guide_generator import UserGuideGenerator, create_sample_protocol_info, create_sample_crf_design
from datetime import datetime


def example_basic_usage():
    """Example 1: Basic usage with sample data"""
    print("=" * 80)
    print("Example 1: Basic User Guide Generation")
    print("=" * 80)

    # Create sample data
    protocol_info = create_sample_protocol_info()
    crf_design = create_sample_crf_design()

    # Initialize generator
    generator = UserGuideGenerator(
        protocol_info=protocol_info,
        crf_design=crf_design,
        system_name="MyClinicalEDC System"
    )

    # Generate user guide
    output_path = "../output/basic_user_guide.docx"
    generator.generate(output_path)

    print(f"\n✓ User guide generated: {output_path}")
    print(f"✓ Screenshot list: {output_path.replace('.docx', '_screenshots.txt')}")


def example_custom_protocol():
    """Example 2: Custom protocol and CRF design"""
    print("\n" + "=" * 80)
    print("Example 2: Custom Protocol User Guide Generation")
    print("=" * 80)

    # Define custom protocol information
    protocol_info = {
        'protocol_id': 'ABC-123-2025',
        'protocol_title': 'A Multicenter Study Evaluating the Efficacy and Safety of Drug XYZ in Treatment-Naive Patients',
        'sponsor': 'Global Pharma Research Inc.',
        'version': '2.1',
        'date': '2025-11-18'
    }

    # Define custom CRF design
    crf_design = {
        'forms': [
            {
                'form_name': 'enrollment',
                'form_title': 'Enrollment Form',
                'visit': 'Screening Visit',
                'fields': [
                    {
                        'field_name': 'screening_number',
                        'field_label': 'Screening Number',
                        'field_type': 'text',
                        'required': True,
                        'validation': 'Format: SCR-XXXX-YYYY'
                    },
                    {
                        'field_name': 'consent_date',
                        'field_label': 'Informed Consent Date',
                        'field_type': 'date',
                        'required': True,
                        'validation': 'Cannot be future date'
                    },
                    {
                        'field_name': 'eligibility_confirmed',
                        'field_label': 'Eligibility Criteria Met?',
                        'field_type': 'radio',
                        'required': True,
                        'validation': 'Yes/No'
                    }
                ]
            },
            {
                'form_name': 'medical_history',
                'form_title': 'Medical History',
                'visit': 'Screening Visit',
                'fields': [
                    {
                        'field_name': 'diabetes',
                        'field_label': 'History of Diabetes',
                        'field_type': 'radio',
                        'required': True,
                        'validation': 'Yes/No'
                    },
                    {
                        'field_name': 'hypertension',
                        'field_label': 'History of Hypertension',
                        'field_type': 'radio',
                        'required': True,
                        'validation': 'Yes/No'
                    },
                    {
                        'field_name': 'cardiovascular',
                        'field_label': 'History of Cardiovascular Disease',
                        'field_type': 'radio',
                        'required': True,
                        'validation': 'Yes/No'
                    },
                    {
                        'field_name': 'other_conditions',
                        'field_label': 'Other Significant Medical Conditions',
                        'field_type': 'textarea',
                        'required': False,
                        'validation': 'Max 1000 characters'
                    }
                ]
            },
            {
                'form_name': 'concomitant_medications',
                'form_title': 'Concomitant Medications',
                'visit': 'All Visits',
                'fields': [
                    {
                        'field_name': 'medication_name',
                        'field_label': 'Medication Name',
                        'field_type': 'text',
                        'required': True,
                        'validation': 'Use generic name when possible'
                    },
                    {
                        'field_name': 'dose',
                        'field_label': 'Dose',
                        'field_type': 'text',
                        'required': True,
                        'validation': 'Include unit (mg, mL, etc.)'
                    },
                    {
                        'field_name': 'frequency',
                        'field_label': 'Frequency',
                        'field_type': 'dropdown',
                        'required': True,
                        'validation': 'QD/BID/TID/QID/PRN/Other'
                    },
                    {
                        'field_name': 'start_date',
                        'field_label': 'Start Date',
                        'field_type': 'date',
                        'required': True,
                        'validation': 'Partial dates allowed'
                    },
                    {
                        'field_name': 'ongoing',
                        'field_label': 'Medication Ongoing?',
                        'field_type': 'radio',
                        'required': True,
                        'validation': 'Yes/No'
                    }
                ]
            },
            {
                'form_name': 'laboratory_results',
                'form_title': 'Laboratory Results',
                'visit': 'Screening, Week 4, Week 8, Week 12',
                'fields': [
                    {
                        'field_name': 'hemoglobin',
                        'field_label': 'Hemoglobin (g/dL)',
                        'field_type': 'decimal',
                        'required': True,
                        'validation': 'Range: 7.0-20.0'
                    },
                    {
                        'field_name': 'wbc',
                        'field_label': 'White Blood Cell Count (10^9/L)',
                        'field_type': 'decimal',
                        'required': True,
                        'validation': 'Range: 1.0-30.0'
                    },
                    {
                        'field_name': 'platelets',
                        'field_label': 'Platelet Count (10^9/L)',
                        'field_type': 'integer',
                        'required': True,
                        'validation': 'Range: 50-800'
                    },
                    {
                        'field_name': 'creatinine',
                        'field_label': 'Serum Creatinine (mg/dL)',
                        'field_type': 'decimal',
                        'required': True,
                        'validation': 'Range: 0.3-5.0'
                    },
                    {
                        'field_name': 'alt',
                        'field_label': 'ALT (U/L)',
                        'field_type': 'integer',
                        'required': True,
                        'validation': 'Range: 5-500'
                    }
                ]
            },
            {
                'form_name': 'efficacy_assessment',
                'form_title': 'Efficacy Assessment',
                'visit': 'Baseline, Week 4, Week 8, Week 12',
                'fields': [
                    {
                        'field_name': 'primary_symptom_score',
                        'field_label': 'Primary Symptom Score',
                        'field_type': 'number',
                        'required': True,
                        'validation': 'Scale: 0-10 (0=none, 10=severe)'
                    },
                    {
                        'field_name': 'quality_of_life_score',
                        'field_label': 'Quality of Life Score',
                        'field_type': 'number',
                        'required': True,
                        'validation': 'Scale: 0-100 (higher is better)'
                    },
                    {
                        'field_name': 'clinical_response',
                        'field_label': 'Clinical Response',
                        'field_type': 'dropdown',
                        'required': True,
                        'validation': 'Complete Response/Partial Response/Stable/Progressive Disease'
                    }
                ]
            }
        ]
    }

    # Initialize generator with custom data
    generator = UserGuideGenerator(
        protocol_info=protocol_info,
        crf_design=crf_design,
        system_name="ClinicalTrials EDC Platform"
    )

    # Generate user guide
    output_path = "../output/custom_user_guide.docx"
    generator.generate(output_path)

    print(f"\n✓ Custom user guide generated: {output_path}")
    print(f"✓ Total pages generated with {len(generator.get_screenshot_list())} screenshot placeholders")


def example_screenshot_management():
    """Example 3: Working with screenshot placeholders"""
    print("\n" + "=" * 80)
    print("Example 3: Screenshot Management")
    print("=" * 80)

    # Create generator
    protocol_info = create_sample_protocol_info()
    crf_design = create_sample_crf_design()

    generator = UserGuideGenerator(
        protocol_info=protocol_info,
        crf_design=crf_design,
        system_name="Research EDC System"
    )

    # Generate user guide
    output_path = "../output/screenshot_example_user_guide.docx"
    generator.generate(output_path)

    # Get screenshot list
    screenshots = generator.get_screenshot_list()

    print(f"\n✓ Generated user guide with {len(screenshots)} screenshot placeholders")
    print("\nScreenshot Requirements:")
    print("-" * 80)

    # Display screenshot requirements grouped by section
    screenshots_by_section = {}
    for screenshot in screenshots:
        if screenshot.section not in screenshots_by_section:
            screenshots_by_section[screenshot.section] = []
        screenshots_by_section[screenshot.section].append(screenshot)

    for section, section_screenshots in screenshots_by_section.items():
        print(f"\n{section} ({len(section_screenshots)} screenshots):")
        for i, screenshot in enumerate(section_screenshots, 1):
            print(f"  {i}. Step: {screenshot.step}")
            print(f"     Description: {screenshot.description}")
            print(f"     Size: {screenshot.width}\" x {screenshot.height}\"")


def example_minimal_crf():
    """Example 4: Minimal CRF design"""
    print("\n" + "=" * 80)
    print("Example 4: Minimal CRF User Guide")
    print("=" * 80)

    protocol_info = {
        'protocol_id': 'SIMPLE-001',
        'protocol_title': 'Simple Trial Protocol',
        'sponsor': 'Research Institute',
        'version': '1.0',
        'date': datetime.now().strftime('%Y-%m-%d')
    }

    # Minimal CRF with just one form
    crf_design = {
        'forms': [
            {
                'form_name': 'baseline_assessment',
                'form_title': 'Baseline Assessment',
                'visit': 'Day 1',
                'fields': [
                    {
                        'field_name': 'assessment_date',
                        'field_label': 'Assessment Date',
                        'field_type': 'date',
                        'required': True,
                        'validation': 'Today or past date'
                    },
                    {
                        'field_name': 'weight',
                        'field_label': 'Weight (kg)',
                        'field_type': 'decimal',
                        'required': True,
                        'validation': 'Range: 30-200'
                    },
                    {
                        'field_name': 'height',
                        'field_label': 'Height (cm)',
                        'field_type': 'decimal',
                        'required': True,
                        'validation': 'Range: 100-250'
                    }
                ]
            }
        ]
    }

    generator = UserGuideGenerator(
        protocol_info=protocol_info,
        crf_design=crf_design,
        system_name="Simple EDC"
    )

    output_path = "../output/minimal_user_guide.docx"
    generator.generate(output_path)

    print(f"\n✓ Minimal user guide generated: {output_path}")


def example_without_appendix():
    """Example 5: Generate user guide without appendix"""
    print("\n" + "=" * 80)
    print("Example 5: User Guide Without Appendix")
    print("=" * 80)

    protocol_info = create_sample_protocol_info()
    crf_design = create_sample_crf_design()

    generator = UserGuideGenerator(
        protocol_info=protocol_info,
        crf_design=crf_design,
        system_name="EDC Pro"
    )

    output_path = "../output/no_appendix_user_guide.docx"
    generator.generate(output_path, include_appendix=False)

    print(f"\n✓ User guide without appendix generated: {output_path}")


def run_all_examples():
    """Run all examples"""
    print("\n")
    print("*" * 80)
    print("EDC/ePRO USER GUIDE GENERATOR - EXAMPLES")
    print("*" * 80)
    print("\n")

    # Create output directory if it doesn't exist
    output_dir = "../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}\n")

    try:
        example_basic_usage()
        example_custom_protocol()
        example_screenshot_management()
        example_minimal_crf()
        example_without_appendix()

        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nGenerated files can be found in the 'output' directory:")
        print("  - basic_user_guide.docx")
        print("  - custom_user_guide.docx")
        print("  - screenshot_example_user_guide.docx")
        print("  - minimal_user_guide.docx")
        print("  - no_appendix_user_guide.docx")
        print("\nScreenshot requirement files (*.txt) are also generated alongside each .docx file.")

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check if user wants to run specific example
    if len(sys.argv) > 1:
        example_num = sys.argv[1]

        examples = {
            '1': example_basic_usage,
            '2': example_custom_protocol,
            '3': example_screenshot_management,
            '4': example_minimal_crf,
            '5': example_without_appendix
        }

        if example_num in examples:
            examples[example_num]()
        else:
            print(f"Unknown example number: {example_num}")
            print("Available examples: 1, 2, 3, 4, 5")
            print("Or run without arguments to execute all examples")
    else:
        # Run all examples
        run_all_examples()
