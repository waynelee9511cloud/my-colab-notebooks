"""
Data Management Plan (DMP) Generator - Example Usage

This file demonstrates how to use the DMP Generator module to create
comprehensive Data Management Plans for clinical trials.

Author: Clinical Doc Automation Team
Date: 2025-11-18
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.dmp_generator import (
    DMPGenerator,
    ProtocolInfo,
    DataManagementRole,
    CRFDomain,
    ValidationCheck,
    Milestone,
    DMPSection,
    create_dmp,
    create_dmp_with_defaults
)


def example_1_basic_dmp():
    """
    Example 1: Create a basic DMP with minimal configuration
    """
    print("\n" + "=" * 80)
    print("Example 1: Basic DMP Generation")
    print("=" * 80)

    # Create protocol information
    protocol_info = ProtocolInfo(
        protocol_number="BASIC-2025-001",
        protocol_title="A Basic Phase II Study Example",
        sponsor="Example Pharma Ltd.",
        indication="Hypertension",
        phase="Phase II",
        version="1.0"
    )

    # Create DMP generator
    generator = DMPGenerator(protocol_info)

    # Generate document
    output_path = "/tmp/examples/DMP_Basic_Example.docx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result = generator.generate_dmp_document(output_path, use_word_formatter=False)
    print(f"\n✓ Basic DMP generated: {result}")
    print(f"  Protocol: {protocol_info.protocol_number}")
    print(f"  Sponsor: {protocol_info.sponsor}")


def example_2_comprehensive_dmp():
    """
    Example 2: Create a comprehensive DMP with all features
    """
    print("\n" + "=" * 80)
    print("Example 2: Comprehensive DMP Generation")
    print("=" * 80)

    # 1. Create detailed protocol information
    protocol_info = ProtocolInfo(
        protocol_number="COMP-2025-002",
        protocol_title="A Phase III, Multicenter, Randomized, Double-Blind, "
                      "Placebo-Controlled Study to Evaluate the Efficacy and Safety "
                      "of Novel Drug in Patients with Type 2 Diabetes Mellitus",
        sponsor="Global Pharmaceutical Research Inc.",
        indication="Type 2 Diabetes Mellitus",
        phase="Phase III",
        study_design="Randomized, Double-Blind, Placebo-Controlled, Parallel Group",
        sample_size="450 subjects (300 active, 150 placebo)",
        study_duration="24 months (18 months enrollment + 6 months treatment)",
        version="2.0"
    )

    # 2. Create DMP generator
    generator = DMPGenerator(protocol_info)

    # 3. Set EDC system
    generator.set_edc_system("Medidata Rave EDC System v2023.1")

    # 4. Add additional DM roles
    generator.add_dm_role(
        DataManagementRole(
            role="Medical Coder",
            organization="Coding Services Inc.",
            responsibilities=[
                "Medical coding of adverse events using MedDRA",
                "Drug coding of concomitant medications using WHO Drug",
                "Quality control of coded data",
                "Maintenance of coding dictionaries"
            ],
            contact_person="Jane Smith",
            contact_email="jane.smith@codingservices.com"
        )
    )

    generator.add_dm_role(
        DataManagementRole(
            role="Database Programmer",
            organization="Global Pharmaceutical Research Inc.",
            responsibilities=[
                "Database build and configuration in EDC system",
                "Edit check programming and testing",
                "Report development for data review",
                "Database extracts for statistical analysis"
            ],
            contact_person="John Doe",
            contact_email="john.doe@globalpharma.com"
        )
    )

    # 5. Add CRF domains
    crf_domains = [
        CRFDomain(
            domain_name="Demographics",
            description="Subject demographic information including age, sex, race, ethnicity",
            visit_schedule=["Screening"],
            is_critical=True,
            validation_rules=8
        ),
        CRFDomain(
            domain_name="Medical History",
            description="Subject medical history including diabetes history and complications",
            visit_schedule=["Screening"],
            is_critical=True,
            validation_rules=12
        ),
        CRFDomain(
            domain_name="Inclusion/Exclusion Criteria",
            description="Assessment of subject eligibility",
            visit_schedule=["Screening"],
            is_critical=True,
            validation_rules=25
        ),
        CRFDomain(
            domain_name="Vital Signs",
            description="Blood pressure, heart rate, respiratory rate, temperature, weight, height",
            visit_schedule=["Screening", "Baseline", "Week 4", "Week 8", "Week 12", "Week 24"],
            is_critical=False,
            validation_rules=18
        ),
        CRFDomain(
            domain_name="Physical Examination",
            description="Complete physical examination by body system",
            visit_schedule=["Screening", "Week 12", "Week 24"],
            is_critical=False,
            validation_rules=10
        ),
        CRFDomain(
            domain_name="Laboratory",
            description="Hematology, chemistry, HbA1c, fasting glucose, lipid panel, urinalysis",
            visit_schedule=["Screening", "Baseline", "Week 4", "Week 8", "Week 12", "Week 24"],
            is_critical=True,
            validation_rules=45
        ),
        CRFDomain(
            domain_name="ECG",
            description="12-lead electrocardiogram",
            visit_schedule=["Screening", "Week 12", "Week 24"],
            is_critical=True,
            validation_rules=15
        ),
        CRFDomain(
            domain_name="Efficacy Assessments",
            description="HbA1c, fasting plasma glucose, weight, BMI",
            visit_schedule=["Baseline", "Week 4", "Week 8", "Week 12", "Week 24"],
            is_critical=True,
            validation_rules=20
        ),
        CRFDomain(
            domain_name="Adverse Events",
            description="All adverse events including serious adverse events",
            visit_schedule=["All visits"],
            is_critical=True,
            validation_rules=35
        ),
        CRFDomain(
            domain_name="Concomitant Medications",
            description="All medications taken during the study period",
            visit_schedule=["All visits"],
            is_critical=True,
            validation_rules=22
        ),
        CRFDomain(
            domain_name="Study Drug Administration",
            description="Study drug dispensing and accountability",
            visit_schedule=["Baseline", "Week 4", "Week 8", "Week 12", "Week 24"],
            is_critical=True,
            validation_rules=18
        ),
        CRFDomain(
            domain_name="Protocol Deviations",
            description="Documentation of any protocol deviations",
            visit_schedule=["As needed"],
            is_critical=True,
            validation_rules=10
        )
    ]

    for domain in crf_domains:
        generator.add_crf_domain(domain)

    # 6. Add study-specific validation checks
    study_validations = [
        ValidationCheck(
            check_type="HbA1c Eligibility Check",
            description="Verify HbA1c ≥ 7.0% and ≤ 10.0% at screening per inclusion criteria",
            severity="Critical",
            implementation="Real-time"
        ),
        ValidationCheck(
            check_type="Diabetes Duration Check",
            description="Verify diabetes diagnosis at least 6 months prior to screening",
            severity="Critical",
            implementation="Real-time"
        ),
        ValidationCheck(
            check_type="Hypoglycemia Event Check",
            description="Flag severe hypoglycemia events (glucose < 54 mg/dL)",
            severity="Critical",
            implementation="Real-time"
        ),
        ValidationCheck(
            check_type="Weight Change Alert",
            description="Alert if weight change > 10% from baseline",
            severity="Major",
            implementation="Batch"
        ),
        ValidationCheck(
            check_type="Visit Window Deviation",
            description="Check if visit occurred within protocol-specified window (±3 days)",
            severity="Major",
            implementation="Batch"
        ),
        ValidationCheck(
            check_type="Drug Compliance Check",
            description="Calculate and flag if compliance < 80% or > 120%",
            severity="Major",
            implementation="Batch"
        )
    ]

    for validation in study_validations:
        generator.add_validation_check(validation)

    # 7. Add project milestones
    milestones = [
        Milestone(
            name="DMP Finalization",
            description="Data Management Plan finalized and approved",
            planned_date="15-Jan-2025",
            responsible="Data Management Lead"
        ),
        Milestone(
            name="Database Design Complete",
            description="CRF design and database build completed",
            planned_date="31-Jan-2025",
            responsible="Clinical Data Manager"
        ),
        Milestone(
            name="UAT Sign-off",
            description="User Acceptance Testing completed and signed off",
            planned_date="15-Feb-2025",
            responsible="Clinical Data Manager & Clinical Team"
        ),
        Milestone(
            name="Database Go-Live",
            description="EDC system activated for data entry",
            planned_date="01-Mar-2025",
            responsible="Database Programmer"
        ),
        Milestone(
            name="First Subject First Visit",
            description="First subject enrolled in the study",
            planned_date="15-Mar-2025",
            responsible="Clinical Operations"
        ),
        Milestone(
            name="50% Enrollment",
            description="50% of target enrollment achieved (225 subjects)",
            planned_date="30-Jun-2025",
            responsible="Clinical Operations"
        ),
        Milestone(
            name="Last Subject First Visit",
            description="Last subject enrolled in the study",
            planned_date="30-Sep-2025",
            responsible="Clinical Operations"
        ),
        Milestone(
            name="Last Subject Last Visit",
            description="Last subject completes final study visit",
            planned_date="31-Mar-2026",
            responsible="Clinical Operations"
        ),
        Milestone(
            name="Database Cleaning Complete",
            description="All data queries resolved, database cleaning complete",
            planned_date="30-Apr-2026",
            responsible="Clinical Data Manager"
        ),
        Milestone(
            name="Database Lock",
            description="Clinical database locked for statistical analysis",
            planned_date="15-May-2026",
            responsible="Data Management Lead"
        ),
        Milestone(
            name="Final Database Archive",
            description="Final database and documentation archived",
            planned_date="30-May-2026",
            responsible="Data Management Lead"
        )
    ]

    for milestone in milestones:
        generator.add_milestone(milestone)

    # 8. Add custom sections
    custom_section_1 = DMPSection(
        section_number="11",
        title="Study-Specific Data Management Considerations",
        content="""
This study has several unique data management considerations that require special attention:

The study involves continuous glucose monitoring (CGM) devices that will collect data electronically.
CGM data will be transferred from devices to a central data repository and integrated with the
clinical database. Special validation rules have been developed to ensure CGM data quality.

Additionally, this study includes Patient-Reported Outcomes (PRO) questionnaires completed via
electronic tablets. PRO data will be transferred nightly to the EDC system and will undergo
automated quality control checks.
        """,
        subsections=[
            {
                'title': 'Continuous Glucose Monitoring (CGM) Data',
                'content': """
CGM devices will be issued to all subjects at baseline. Data will be collected continuously
and uploaded to the CGM vendor's portal. Data transfers from the CGM portal to the clinical
database will occur weekly. Validation rules specific to CGM data include:

• Data completeness checks (minimum 70% of readings per week)
• Device malfunction detection (consecutive identical readings)
• Physiologically implausible values (< 40 mg/dL or > 400 mg/dL)
• Comparison with clinic laboratory glucose values
"""
            },
            {
                'title': 'Patient-Reported Outcomes (PRO)',
                'content': """
PRO questionnaires will be administered electronically at baseline, Week 12, and Week 24:

• Diabetes Treatment Satisfaction Questionnaire (DTSQ)
• EQ-5D-5L Quality of Life Questionnaire
• Hypoglycemia Fear Survey (HFS-II)

All PRO instruments have been validated and will be implemented in the ePRO system exactly
as published. Missing item handling will follow instrument-specific guidelines.
"""
            },
            {
                'title': 'Central Laboratory Data',
                'content': """
All laboratory samples will be analyzed at a central laboratory. Laboratory data will be
transferred electronically to the EDC system using CDISC LAB standard format. Data transfers
will occur within 48 hours of sample analysis. Reconciliation between expected and received
samples will be performed weekly.
"""
            }
        ]
    )

    generator.add_custom_section(custom_section_1)

    custom_section_2 = DMPSection(
        section_number="12",
        title="COVID-19 Pandemic Considerations",
        content="""
In response to the COVID-19 pandemic, this study has implemented remote data collection
procedures to minimize in-person visits while maintaining data quality and subject safety.
        """,
        subsections=[
            {
                'title': 'Remote Visits',
                'content': """
Selected study visits may be conducted remotely via telemedicine when in-person visits
are not feasible due to pandemic restrictions. For remote visits:

• Video or telephone consultations will be used for assessment
• Vital signs may be collected using home monitoring devices
• Laboratory samples may be collected at local facilities
• All remote visit procedures will be documented in the eCRF with visit type indicator
"""
            },
            {
                'title': 'Home Health Visits',
                'content': """
Home health nursing visits may be arranged for subjects unable to travel to the clinic.
Data collected during home visits will be entered into the EDC system with appropriate
visit location documentation.
"""
            }
        ]
    )

    generator.add_custom_section(custom_section_2)

    # 9. Generate comprehensive DMP document
    output_path = "/tmp/examples/DMP_Comprehensive_Example.docx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result = generator.generate_dmp_document(output_path, use_word_formatter=False)

    print(f"\n✓ Comprehensive DMP generated: {result}")
    print(f"\nDocument Statistics:")
    print(f"  - Protocol: {protocol_info.protocol_number}")
    print(f"  - DM Roles: {len(generator.dm_roles)}")
    print(f"  - CRF Domains: {len(generator.crf_domains)}")
    print(f"  - Validation Checks: {len(generator.validation_checks)}")
    print(f"  - Milestones: {len(generator.milestones)}")
    print(f"  - Custom Sections: {len(generator.custom_sections)}")

    # 10. Export configuration to dictionary
    config_dict = generator.export_to_dict()
    print(f"\n✓ DMP configuration exported to dictionary")


def example_3_quick_create():
    """
    Example 3: Quick DMP creation with convenience function
    """
    print("\n" + "=" * 80)
    print("Example 3: Quick DMP Creation with Convenience Function")
    print("=" * 80)

    output_path = "/tmp/examples/DMP_Quick_Create.docx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create DMP with just a few parameters
    result = create_dmp_with_defaults(
        protocol_number="QUICK-2025-003",
        protocol_title="A Quick Example Phase I Study",
        sponsor="Quick Pharma Inc.",
        indication="Healthy Volunteers",
        phase="Phase I",
        output_path=output_path
    )

    print(f"\n✓ Quick DMP generated: {result}")
    print("  This method is perfect for rapid DMP creation with default settings")


def example_4_custom_roles_and_responsibilities():
    """
    Example 4: DMP with custom roles and responsibilities
    """
    print("\n" + "=" * 80)
    print("Example 4: DMP with Custom Roles and Responsibilities")
    print("=" * 80)

    protocol_info = ProtocolInfo(
        protocol_number="CUSTOM-2025-004",
        protocol_title="A Study with Custom Data Management Structure",
        sponsor="Custom Research Organization",
        indication="Oncology",
        phase="Phase II",
        version="1.0"
    )

    generator = DMPGenerator(protocol_info)

    # Clear default roles and add custom roles
    generator.dm_roles = []

    # Add custom organizational structure
    custom_roles = [
        DataManagementRole(
            role="Global Data Management Director",
            organization="Custom Research Organization",
            responsibilities=[
                "Strategic oversight of all data management activities",
                "Approval of DMP and major amendments",
                "Resolution of escalated issues",
                "Liaison with regulatory authorities on data matters"
            ],
            contact_person="Dr. Sarah Johnson",
            contact_email="s.johnson@custom-research.com"
        ),
        DataManagementRole(
            role="Regional Data Manager - North America",
            organization="Custom Research Organization - NA Region",
            responsibilities=[
                "Data management oversight for North American sites",
                "CRF design for region-specific assessments",
                "Regional data review and quality control",
                "Site training on data entry procedures"
            ],
            contact_person="Michael Chen",
            contact_email="m.chen@custom-research.com"
        ),
        DataManagementRole(
            role="Regional Data Manager - Europe",
            organization="Custom Research Organization - EU Region",
            responsibilities=[
                "Data management oversight for European sites",
                "GDPR compliance monitoring",
                "Regional data review and quality control",
                "Site training on data entry procedures"
            ],
            contact_person="Emma Williams",
            contact_email="e.williams@custom-research.eu"
        ),
        DataManagementRole(
            role="Safety Data Manager",
            organization="Custom Research Organization",
            responsibilities=[
                "Adverse event and SAE data review",
                "Safety data quality control",
                "Coordination with pharmacovigilance team",
                "Safety database reconciliation"
            ],
            contact_person="Dr. Robert Martinez",
            contact_email="r.martinez@custom-research.com"
        ),
        DataManagementRole(
            role="EDC System Administrator",
            organization="Technology Services Division",
            responsibilities=[
                "EDC system configuration and maintenance",
                "User account management",
                "System backup and disaster recovery",
                "Technical support for users"
            ],
            contact_person="Alex Taylor",
            contact_email="a.taylor@tech-services.com"
        )
    ]

    for role in custom_roles:
        generator.add_dm_role(role)

    # Generate DMP
    output_path = "/tmp/examples/DMP_Custom_Roles.docx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result = generator.generate_dmp_document(output_path, use_word_formatter=False)

    print(f"\n✓ DMP with custom roles generated: {result}")
    print(f"  Custom roles defined: {len(generator.dm_roles)}")


def example_5_oncology_study():
    """
    Example 5: Oncology study with tumor assessment and imaging data
    """
    print("\n" + "=" * 80)
    print("Example 5: Oncology Study DMP")
    print("=" * 80)

    protocol_info = ProtocolInfo(
        protocol_number="ONCO-2025-005",
        protocol_title="A Phase II Study of Novel Checkpoint Inhibitor in "
                      "Patients with Advanced Non-Small Cell Lung Cancer",
        sponsor="Oncology Research Institute",
        indication="Non-Small Cell Lung Cancer (NSCLC)",
        phase="Phase II",
        study_design="Single-arm, Open-label",
        sample_size="60 subjects",
        study_duration="36 months",
        version="1.0"
    )

    generator = DMPGenerator(protocol_info)
    generator.set_edc_system("Oracle Clinical EDC")

    # Add oncology-specific CRF domains
    onco_domains = [
        CRFDomain(
            domain_name="Tumor Assessment (RECIST 1.1)",
            description="Tumor measurements per RECIST 1.1 criteria",
            visit_schedule=["Baseline", "Every 8 weeks"],
            is_critical=True,
            validation_rules=30
        ),
        CRFDomain(
            domain_name="Imaging Data",
            description="CT scan and other imaging results",
            visit_schedule=["Baseline", "Every 8 weeks"],
            is_critical=True,
            validation_rules=15
        ),
        CRFDomain(
            domain_name="ECOG Performance Status",
            description="Eastern Cooperative Oncology Group performance status",
            visit_schedule=["All visits"],
            is_critical=True,
            validation_rules=5
        ),
        CRFDomain(
            domain_name="Prior Cancer Therapy",
            description="Previous cancer treatments including surgery, radiation, chemotherapy",
            visit_schedule=["Screening"],
            is_critical=True,
            validation_rules=20
        ),
        CRFDomain(
            domain_name="Biomarker Data",
            description="PD-L1 expression, tumor mutation burden",
            visit_schedule=["Screening"],
            is_critical=True,
            validation_rules=12
        )
    ]

    for domain in onco_domains:
        generator.add_crf_domain(domain)

    # Add oncology-specific validations
    onco_validations = [
        ValidationCheck(
            check_type="RECIST Target Lesion Check",
            description="Verify at least 1 and maximum 5 target lesions per RECIST 1.1",
            severity="Critical",
            implementation="Real-time"
        ),
        ValidationCheck(
            check_type="Tumor Assessment Consistency",
            description="Check consistency between radiologist assessment and investigator assessment",
            severity="Major",
            implementation="Batch"
        ),
        ValidationCheck(
            check_type="Progression-Free Survival Calculation",
            description="Verify PFS calculation based on RECIST criteria",
            severity="Critical",
            implementation="Batch"
        ),
        ValidationCheck(
            check_type="Immune-Related Adverse Events",
            description="Flag potential immune-related AEs for special attention",
            severity="Critical",
            implementation="Real-time"
        )
    ]

    for validation in onco_validations:
        generator.add_validation_check(validation)

    # Add oncology-specific custom section
    onco_section = DMPSection(
        section_number="11",
        title="Oncology Study-Specific Procedures",
        content="This section describes data management procedures specific to this oncology clinical trial.",
        subsections=[
            {
                'title': 'Central Imaging Review',
                'content': """
All imaging scans (CT, MRI) will be reviewed centrally by an independent radiology core laboratory.
Image data will be transferred electronically to the imaging vendor. The vendor will perform tumor
measurements according to RECIST 1.1 criteria and transfer results to the EDC system within 5
business days of image acquisition. Reconciliation between site-reported and centrally-reviewed
assessments will be performed for all discrepancies.
"""
            },
            {
                'title': 'Response Evaluation Criteria',
                'content': """
Tumor response will be evaluated according to RECIST 1.1 criteria:
• Complete Response (CR): Disappearance of all target lesions
• Partial Response (PR): ≥30% decrease in sum of diameters of target lesions
• Progressive Disease (PD): ≥20% increase in sum of diameters of target lesions
• Stable Disease (SD): Neither PR nor PD criteria met

Response determinations will be automatically calculated based on tumor measurement data.
Manual review will be performed for all PR and CR determinations.
"""
            },
            {
                'title': 'Biomarker Data Management',
                'content': """
Biomarker samples will be collected at screening and analyzed at a central laboratory.
PD-L1 expression (Tumor Proportion Score) and tumor mutation burden will be determined.
Results will be integrated into the clinical database and used for stratification analysis.
"""
            }
        ]
    )

    generator.add_custom_section(onco_section)

    # Generate DMP
    output_path = "/tmp/examples/DMP_Oncology_Example.docx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result = generator.generate_dmp_document(output_path, use_word_formatter=False)

    print(f"\n✓ Oncology DMP generated: {result}")
    print(f"  Oncology-specific domains: {len([d for d in generator.crf_domains if 'Tumor' in d.domain_name or 'ECOG' in d.domain_name])}")


def run_all_examples():
    """Run all examples"""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "DMP Generator - All Examples" + " " * 30 + "║")
    print("╚" + "=" * 78 + "╝")

    try:
        example_1_basic_dmp()
        example_2_comprehensive_dmp()
        example_3_quick_create()
        example_4_custom_roles_and_responsibilities()
        example_5_oncology_study()

        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80)
        print("\nGenerated files are in: /tmp/examples/")
        print("\nYou can open these .docx files in Microsoft Word or LibreOffice.")

    except Exception as e:
        print(f"\n✗ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num == "1":
            example_1_basic_dmp()
        elif example_num == "2":
            example_2_comprehensive_dmp()
        elif example_num == "3":
            example_3_quick_create()
        elif example_num == "4":
            example_4_custom_roles_and_responsibilities()
        elif example_num == "5":
            example_5_oncology_study()
        elif example_num == "all":
            run_all_examples()
        else:
            print("Unknown example number. Use: 1, 2, 3, 4, 5, or all")
    else:
        # Run all examples by default
        run_all_examples()
