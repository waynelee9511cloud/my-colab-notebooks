"""
CRF Generator - Unit Tests

Simple test script to verify CRF Generator functionality.
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from crf_generator import CRFGenerator, CRFDomain


def test_1_basic_initialization():
    """Test 1: Basic generator initialization."""
    print("\n[Test 1] Basic Initialization")
    print("-" * 50)

    try:
        generator = CRFGenerator()
        print("✓ CRFGenerator initialized successfully")

        protocol_info = {
            'study_title': 'Test Study',
            'protocol_number': 'TEST-001',
            'sponsor': 'Test Sponsor',
            'version': '1.0'
        }
        generator_with_info = CRFGenerator(protocol_info)
        print("✓ CRFGenerator with protocol_info initialized successfully")

        return True
    except Exception as e:
        print(f"✗ Initialization failed: {str(e)}")
        return False


def test_2_standard_domains():
    """Test 2: Verify standard domains."""
    print("\n[Test 2] Standard Domains Verification")
    print("-" * 50)

    try:
        generator = CRFGenerator()

        expected_domains = [
            'demographics',
            'medical_history',
            'vital_signs',
            'laboratory_tests',
            'adverse_events',
            'concomitant_medications',
            'study_drug_administration'
        ]

        for domain in expected_domains:
            if domain in generator.STANDARD_DOMAINS:
                print(f"✓ Domain '{domain}' found")
            else:
                print(f"✗ Domain '{domain}' missing")
                return False

        print(f"\n✓ All {len(expected_domains)} standard domains verified")
        return True
    except Exception as e:
        print(f"✗ Domain verification failed: {str(e)}")
        return False


def test_3_domain_validation():
    """Test 3: Domain validation."""
    print("\n[Test 3] Domain Validation")
    print("-" * 50)

    try:
        # Valid domain
        valid_domain = CRFDomain(
            name='Test Domain',
            description='Test description',
            fields=[
                {
                    'name': 'test_field',
                    'label': 'Test Field',
                    'type': 'text',
                    'required': True
                }
            ]
        )

        if valid_domain.validate():
            print("✓ Valid domain passed validation")
        else:
            print("✗ Valid domain failed validation")
            return False

        # Invalid domain (missing required field key)
        invalid_domain = CRFDomain(
            name='Invalid Domain',
            description='Test',
            fields=[
                {
                    'name': 'test_field',
                    # missing 'label' and 'type'
                }
            ]
        )

        if not invalid_domain.validate():
            print("✓ Invalid domain correctly failed validation")
        else:
            print("✗ Invalid domain incorrectly passed validation")
            return False

        return True
    except Exception as e:
        print(f"✗ Validation test failed: {str(e)}")
        return False


def test_4_custom_domain():
    """Test 4: Add custom domain."""
    print("\n[Test 4] Custom Domain Addition")
    print("-" * 50)

    try:
        generator = CRFGenerator()

        custom_domain = CRFDomain(
            name='Custom Test Domain',
            description='A custom test domain',
            fields=[
                {
                    'name': 'custom_field1',
                    'label': 'Custom Field 1',
                    'type': 'text',
                    'required': True,
                    'coding_instruction': 'Test instruction'
                },
                {
                    'name': 'custom_field2',
                    'label': 'Custom Field 2',
                    'type': 'dropdown',
                    'required': False,
                    'options': ['Option A', 'Option B', 'Option C'],
                    'coding_instruction': 'Select one option'
                }
            ]
        )

        result = generator.add_custom_domain(custom_domain)

        if result:
            print("✓ Custom domain added successfully")

            # Verify it's in the custom_domains dict
            if 'custom_test_domain' in generator.custom_domains:
                print("✓ Custom domain found in generator.custom_domains")
            else:
                print("✗ Custom domain not found in generator.custom_domains")
                return False

            return True
        else:
            print("✗ Failed to add custom domain")
            return False
    except Exception as e:
        print(f"✗ Custom domain test failed: {str(e)}")
        return False


def test_5_get_available_domains():
    """Test 5: Get available domains."""
    print("\n[Test 5] Get Available Domains")
    print("-" * 50)

    try:
        generator = CRFGenerator()

        # Add a custom domain
        custom_domain = CRFDomain(
            name='Test Custom',
            description='Test',
            fields=[
                {
                    'name': 'field1',
                    'label': 'Field 1',
                    'type': 'text',
                    'required': True
                }
            ]
        )
        generator.add_custom_domain(custom_domain)

        # Get available domains
        available = generator.get_available_domains()

        print(f"Found {len(available)} domains:")
        for domain in available:
            print(f"  - {domain}")

        # Should have 7 standard + 1 custom = 8
        if len(available) >= 8:
            print(f"✓ Expected number of domains found ({len(available)})")
            return True
        else:
            print(f"✗ Unexpected number of domains: {len(available)}")
            return False
    except Exception as e:
        print(f"✗ Get domains test failed: {str(e)}")
        return False


def test_6_crf_generation():
    """Test 6: Generate actual CRF document."""
    print("\n[Test 6] CRF Document Generation")
    print("-" * 50)

    try:
        protocol_info = {
            'study_title': 'Test Clinical Trial',
            'protocol_number': 'TEST-2025-001',
            'sponsor': 'Test Research Institute',
            'version': '1.0'
        }

        generator = CRFGenerator(protocol_info)

        # Create test output directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'test')
        os.makedirs(output_dir, exist_ok=True)

        # Generate CRF with selected domains
        output_path = os.path.join(output_dir, f'test_CRF_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx')

        crf_file = generator.generate_crf(
            domains=['demographics', 'vital_signs', 'adverse_events'],
            output_path=output_path
        )

        # Check if file was created
        if os.path.exists(crf_file):
            file_size = os.path.getsize(crf_file)
            print(f"✓ CRF file created: {crf_file}")
            print(f"✓ File size: {file_size:,} bytes")

            if file_size > 0:
                print("✓ File is not empty")
                return True
            else:
                print("✗ File is empty")
                return False
        else:
            print(f"✗ CRF file not created at: {crf_file}")
            return False
    except Exception as e:
        print(f"✗ CRF generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_7_domain_template_export():
    """Test 7: Export domain template."""
    print("\n[Test 7] Domain Template Export")
    print("-" * 50)

    try:
        generator = CRFGenerator()

        # Create test output directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'test')
        os.makedirs(output_dir, exist_ok=True)

        # Export adverse events template
        template_path = os.path.join(output_dir, 'adverse_events_template_test.docx')

        result = generator.export_domain_template('adverse_events', template_path)

        if result and os.path.exists(template_path):
            file_size = os.path.getsize(template_path)
            print(f"✓ Template exported: {template_path}")
            print(f"✓ File size: {file_size:,} bytes")
            return True
        else:
            print(f"✗ Template export failed")
            return False
    except Exception as e:
        print(f"✗ Template export test failed: {str(e)}")
        return False


def test_8_field_types():
    """Test 8: All field types representation."""
    print("\n[Test 8] Field Types Coverage")
    print("-" * 50)

    try:
        # Create domain with all field types
        all_types_domain = CRFDomain(
            name='All Field Types Test',
            description='Testing all supported field types',
            fields=[
                {
                    'name': 'text_field',
                    'label': 'Text Field',
                    'type': 'text',
                    'required': True,
                    'coding_instruction': 'Enter text'
                },
                {
                    'name': 'numeric_field',
                    'label': 'Numeric Field',
                    'type': 'numeric',
                    'required': True,
                    'unit': 'mg',
                    'coding_instruction': 'Enter number'
                },
                {
                    'name': 'date_field',
                    'label': 'Date Field',
                    'type': 'date',
                    'required': True,
                    'coding_instruction': 'Enter date'
                },
                {
                    'name': 'checkbox_field',
                    'label': 'Checkbox Field',
                    'type': 'checkbox',
                    'required': True,
                    'options': ['Yes', 'No'],
                    'coding_instruction': 'Check applicable'
                },
                {
                    'name': 'dropdown_field',
                    'label': 'Dropdown Field',
                    'type': 'dropdown',
                    'required': True,
                    'options': ['Option 1', 'Option 2', 'Option 3'],
                    'coding_instruction': 'Select one'
                }
            ]
        )

        if all_types_domain.validate():
            print("✓ All field types domain validated")

            # Generate CRF with this domain
            protocol_info = {'study_title': 'Field Types Test', 'protocol_number': 'TEST-FT', 'sponsor': 'Test', 'version': '1.0'}
            generator = CRFGenerator(protocol_info)
            generator.add_custom_domain(all_types_domain)

            output_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'test')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'field_types_test.docx')

            generator.generate_crf(
                domains=['all_field_types_test'],
                output_path=output_path
            )

            if os.path.exists(output_path):
                print(f"✓ CRF with all field types generated: {output_path}")
                return True
            else:
                print("✗ CRF generation failed")
                return False
        else:
            print("✗ Domain validation failed")
            return False
    except Exception as e:
        print(f"✗ Field types test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results."""

    print("="*80)
    print("CRF GENERATOR - TEST SUITE")
    print("="*80)

    tests = [
        test_1_basic_initialization,
        test_2_standard_domains,
        test_3_domain_validation,
        test_4_custom_domain,
        test_5_get_available_domains,
        test_6_crf_generation,
        test_7_domain_template_export,
        test_8_field_types
    ]

    results = []

    for i, test_func in enumerate(tests, 1):
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"\n✗ Test {i} crashed: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_func.__name__, False))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nTests Passed: {passed}/{total}")
    print("\nDetailed Results:")

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test_name}")

    print("\n" + "="*80)

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️  {total - passed} TEST(S) FAILED")

    print("="*80 + "\n")

    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
