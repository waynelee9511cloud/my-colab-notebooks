"""
Test Suite for Data Management Plan (DMP) Generator

This module contains comprehensive tests for the DMP Generator functionality.

Author: Clinical Doc Automation Team
Date: 2025-11-18
"""

import unittest
import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
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


class TestProtocolInfo(unittest.TestCase):
    """Test ProtocolInfo class"""

    def test_protocol_info_creation(self):
        """Test creating ProtocolInfo object"""
        protocol = ProtocolInfo(
            protocol_number="TEST-001",
            protocol_title="Test Protocol",
            sponsor="Test Sponsor",
            indication="Test Indication",
            phase="Phase I"
        )

        self.assertEqual(protocol.protocol_number, "TEST-001")
        self.assertEqual(protocol.protocol_title, "Test Protocol")
        self.assertEqual(protocol.sponsor, "Test Sponsor")
        self.assertEqual(protocol.indication, "Test Indication")
        self.assertEqual(protocol.phase, "Phase I")
        self.assertIsNotNone(protocol.date)  # Auto-generated date

    def test_protocol_info_with_optional_fields(self):
        """Test ProtocolInfo with optional fields"""
        protocol = ProtocolInfo(
            protocol_number="TEST-002",
            protocol_title="Test Protocol 2",
            sponsor="Test Sponsor 2",
            indication="Test Indication 2",
            phase="Phase II",
            study_design="Randomized",
            sample_size="100",
            study_duration="12 months",
            version="2.0",
            date="01-Jan-2025"
        )

        self.assertEqual(protocol.study_design, "Randomized")
        self.assertEqual(protocol.sample_size, "100")
        self.assertEqual(protocol.study_duration, "12 months")
        self.assertEqual(protocol.version, "2.0")
        self.assertEqual(protocol.date, "01-Jan-2025")


class TestDataManagementRole(unittest.TestCase):
    """Test DataManagementRole class"""

    def test_role_creation(self):
        """Test creating DataManagementRole object"""
        role = DataManagementRole(
            role="Test Role",
            organization="Test Org",
            responsibilities=["Task 1", "Task 2"]
        )

        self.assertEqual(role.role, "Test Role")
        self.assertEqual(role.organization, "Test Org")
        self.assertEqual(len(role.responsibilities), 2)
        self.assertIsNone(role.contact_person)
        self.assertIsNone(role.contact_email)

    def test_role_with_contact_info(self):
        """Test role with contact information"""
        role = DataManagementRole(
            role="Test Role",
            organization="Test Org",
            responsibilities=["Task 1"],
            contact_person="John Doe",
            contact_email="john@example.com"
        )

        self.assertEqual(role.contact_person, "John Doe")
        self.assertEqual(role.contact_email, "john@example.com")


class TestCRFDomain(unittest.TestCase):
    """Test CRFDomain class"""

    def test_domain_creation(self):
        """Test creating CRFDomain object"""
        domain = CRFDomain(
            domain_name="Demographics",
            description="Subject demographics",
            visit_schedule=["Screening", "Baseline"]
        )

        self.assertEqual(domain.domain_name, "Demographics")
        self.assertEqual(domain.description, "Subject demographics")
        self.assertEqual(len(domain.visit_schedule), 2)
        self.assertFalse(domain.is_critical)
        self.assertEqual(domain.validation_rules, 0)

    def test_critical_domain(self):
        """Test critical domain"""
        domain = CRFDomain(
            domain_name="Adverse Events",
            description="AE data",
            visit_schedule=["All visits"],
            is_critical=True,
            validation_rules=25
        )

        self.assertTrue(domain.is_critical)
        self.assertEqual(domain.validation_rules, 25)


class TestValidationCheck(unittest.TestCase):
    """Test ValidationCheck class"""

    def test_validation_check_creation(self):
        """Test creating ValidationCheck object"""
        check = ValidationCheck(
            check_type="Range Check",
            description="Test range check",
            severity="Major",
            implementation="Real-time"
        )

        self.assertEqual(check.check_type, "Range Check")
        self.assertEqual(check.description, "Test range check")
        self.assertEqual(check.severity, "Major")
        self.assertEqual(check.implementation, "Real-time")


class TestMilestone(unittest.TestCase):
    """Test Milestone class"""

    def test_milestone_creation(self):
        """Test creating Milestone object"""
        milestone = Milestone(
            name="Database Lock",
            description="Lock the database",
            planned_date="31-Dec-2025",
            responsible="DM Lead"
        )

        self.assertEqual(milestone.name, "Database Lock")
        self.assertEqual(milestone.description, "Lock the database")
        self.assertEqual(milestone.planned_date, "31-Dec-2025")
        self.assertEqual(milestone.responsible, "DM Lead")
        self.assertEqual(milestone.status, "Planned")


class TestDMPSection(unittest.TestCase):
    """Test DMPSection class"""

    def test_section_creation(self):
        """Test creating DMPSection object"""
        section = DMPSection(
            section_number="11",
            title="Custom Section",
            content="Custom content"
        )

        self.assertEqual(section.section_number, "11")
        self.assertEqual(section.title, "Custom Section")
        self.assertEqual(section.content, "Custom content")
        self.assertEqual(len(section.subsections), 0)

    def test_section_with_subsections(self):
        """Test section with subsections"""
        section = DMPSection(
            section_number="11",
            title="Custom Section",
            content="Custom content",
            subsections=[
                {'title': 'Subsection 1', 'content': 'Content 1'},
                {'title': 'Subsection 2', 'content': 'Content 2'}
            ]
        )

        self.assertEqual(len(section.subsections), 2)
        self.assertEqual(section.subsections[0]['title'], 'Subsection 1')


class TestDMPGenerator(unittest.TestCase):
    """Test DMPGenerator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.protocol_info = ProtocolInfo(
            protocol_number="TEST-001",
            protocol_title="Test Protocol",
            sponsor="Test Sponsor",
            indication="Test Indication",
            phase="Phase I"
        )
        self.generator = DMPGenerator(self.protocol_info)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_generator_initialization(self):
        """Test DMP generator initialization"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.protocol_info.protocol_number, "TEST-001")
        self.assertGreater(len(self.generator.dm_roles), 0)  # Default roles
        self.assertGreater(len(self.generator.validation_checks), 0)  # Default checks
        self.assertGreater(len(self.generator.database_lock_criteria), 0)  # Default criteria

    def test_add_dm_role(self):
        """Test adding DM role"""
        initial_count = len(self.generator.dm_roles)

        role = DataManagementRole(
            role="Test Role",
            organization="Test Org",
            responsibilities=["Task 1"]
        )

        self.generator.add_dm_role(role)
        self.assertEqual(len(self.generator.dm_roles), initial_count + 1)

    def test_add_crf_domain(self):
        """Test adding CRF domain"""
        self.assertEqual(len(self.generator.crf_domains), 0)

        domain = CRFDomain(
            domain_name="Demographics",
            description="Subject demographics",
            visit_schedule=["Screening"]
        )

        self.generator.add_crf_domain(domain)
        self.assertEqual(len(self.generator.crf_domains), 1)

    def test_add_validation_check(self):
        """Test adding validation check"""
        initial_count = len(self.generator.validation_checks)

        check = ValidationCheck(
            check_type="Custom Check",
            description="Test check",
            severity="Major",
            implementation="Real-time"
        )

        self.generator.add_validation_check(check)
        self.assertEqual(len(self.generator.validation_checks), initial_count + 1)

    def test_add_milestone(self):
        """Test adding milestone"""
        self.assertEqual(len(self.generator.milestones), 0)

        milestone = Milestone(
            name="Test Milestone",
            description="Test",
            planned_date="01-Jan-2025",
            responsible="Tester"
        )

        self.generator.add_milestone(milestone)
        self.assertEqual(len(self.generator.milestones), 1)

    def test_add_custom_section(self):
        """Test adding custom section"""
        self.assertEqual(len(self.generator.custom_sections), 0)

        section = DMPSection(
            section_number="11",
            title="Custom Section",
            content="Custom content"
        )

        self.generator.add_custom_section(section)
        self.assertEqual(len(self.generator.custom_sections), 1)

    def test_set_edc_system(self):
        """Test setting EDC system"""
        self.generator.set_edc_system("Test EDC")
        self.assertEqual(self.generator.edc_system, "Test EDC")

    def test_export_to_dict(self):
        """Test exporting to dictionary"""
        export_dict = self.generator.export_to_dict()

        self.assertIn('protocol_info', export_dict)
        self.assertIn('dm_roles', export_dict)
        self.assertIn('crf_domains', export_dict)
        self.assertIn('validation_checks', export_dict)
        self.assertIn('milestones', export_dict)

        self.assertEqual(export_dict['protocol_info']['protocol_number'], "TEST-001")

    def test_generate_dmp_document(self):
        """Test generating DMP document"""
        output_path = os.path.join(self.temp_dir, "test_dmp.docx")

        result = self.generator.generate_dmp_document(
            output_path,
            use_word_formatter=False
        )

        self.assertEqual(result, output_path)
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)

    def test_generate_dmp_with_all_components(self):
        """Test generating DMP with all components added"""
        # Add components
        self.generator.add_crf_domain(CRFDomain(
            domain_name="Test Domain",
            description="Test",
            visit_schedule=["V1"]
        ))

        self.generator.add_milestone(Milestone(
            name="Test Milestone",
            description="Test",
            planned_date="01-Jan-2025",
            responsible="Tester"
        ))

        self.generator.add_custom_section(DMPSection(
            section_number="11",
            title="Custom",
            content="Content"
        ))

        # Generate document
        output_path = os.path.join(self.temp_dir, "test_dmp_full.docx")
        result = self.generator.generate_dmp_document(
            output_path,
            use_word_formatter=False
        )

        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_create_dmp(self):
        """Test create_dmp convenience function"""
        protocol_info = ProtocolInfo(
            protocol_number="CONV-001",
            protocol_title="Convenience Test",
            sponsor="Test Sponsor",
            indication="Test",
            phase="Phase I"
        )

        output_path = os.path.join(self.temp_dir, "convenience_dmp.docx")

        result = create_dmp(
            protocol_info=protocol_info,
            output_path=output_path,
            use_word_formatter=False
        )

        self.assertTrue(os.path.exists(result))

    def test_create_dmp_with_components(self):
        """Test create_dmp with additional components"""
        protocol_info = ProtocolInfo(
            protocol_number="CONV-002",
            protocol_title="Convenience Test 2",
            sponsor="Test Sponsor",
            indication="Test",
            phase="Phase II"
        )

        domains = [
            CRFDomain(
                domain_name="Demographics",
                description="Demographics",
                visit_schedule=["Screening"]
            )
        ]

        milestones = [
            Milestone(
                name="Database Lock",
                description="Lock DB",
                planned_date="31-Dec-2025",
                responsible="DM"
            )
        ]

        output_path = os.path.join(self.temp_dir, "convenience_dmp_2.docx")

        result = create_dmp(
            protocol_info=protocol_info,
            output_path=output_path,
            crf_domains=domains,
            milestones=milestones,
            edc_system="Test EDC",
            use_word_formatter=False
        )

        self.assertTrue(os.path.exists(result))

    def test_create_dmp_with_defaults(self):
        """Test create_dmp_with_defaults function"""
        output_path = os.path.join(self.temp_dir, "default_dmp.docx")

        result = create_dmp_with_defaults(
            protocol_number="DEFAULT-001",
            protocol_title="Default Test",
            sponsor="Default Sponsor",
            indication="Default Indication",
            phase="Phase III",
            output_path=output_path
        )

        self.assertTrue(os.path.exists(result))


class TestDocumentStructure(unittest.TestCase):
    """Test document structure and content"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.protocol_info = ProtocolInfo(
            protocol_number="STRUCT-001",
            protocol_title="Structure Test",
            sponsor="Test Sponsor",
            indication="Test",
            phase="Phase I"
        )

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_standard_sections_present(self):
        """Test that all standard sections are included"""
        generator = DMPGenerator(self.protocol_info)

        # Verify standard sections are defined
        self.assertEqual(len(DMPGenerator.STANDARD_SECTIONS), 10)
        self.assertIn("1. Introduction", DMPGenerator.STANDARD_SECTIONS)
        self.assertIn("2. Study Overview", DMPGenerator.STANDARD_SECTIONS)
        self.assertIn("10. Archive", DMPGenerator.STANDARD_SECTIONS)

    def test_default_components_created(self):
        """Test that default components are created"""
        generator = DMPGenerator(self.protocol_info)

        # Check default DM roles
        self.assertGreater(len(generator.dm_roles), 0)
        role_names = [role.role for role in generator.dm_roles]
        self.assertIn("Data Management Lead", role_names)
        self.assertIn("Clinical Data Manager", role_names)

        # Check default validation checks
        self.assertGreater(len(generator.validation_checks), 0)

        # Check default database lock criteria
        self.assertGreater(len(generator.database_lock_criteria), 0)


def run_tests(verbosity=2):
    """
    Run all tests

    Args:
        verbosity: Test output verbosity (1=quiet, 2=normal, 3=verbose)
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestDataManagementRole))
    suite.addTests(loader.loadTestsFromTestCase(TestCRFDomain))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestMilestone))
    suite.addTests(loader.loadTestsFromTestCase(TestDMPSection))
    suite.addTests(loader.loadTestsFromTestCase(TestDMPGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentStructure))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("Test Summary:")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    import sys

    # Parse command line arguments
    verbosity = 2
    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            verbosity = 3
        elif sys.argv[1] == "-q":
            verbosity = 1

    # Run tests
    success = run_tests(verbosity=verbosity)

    # Exit with appropriate code
    sys.exit(0 if success else 1)
