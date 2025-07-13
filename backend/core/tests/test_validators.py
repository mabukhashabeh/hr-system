from datetime import date

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from core.validators import (
    AgeValidator,
    ExperienceValidator,
    FileSizeValidator,
    FileTypeValidator,
    PhoneNumberValidator,
    age_validator,
    experience_validator,
    file_size_validator,
    file_type_validator,
    phone_number_validator,
)


def subtract_years(original_date, years):
    """Subtract years from a date, accounting for leap years."""
    try:
        return original_date.replace(year=original_date.year - years)
    except ValueError:
        # Handle February 29 for non-leap years
        return original_date.replace(month=2, day=28, year=original_date.year - years)


class TestFileSizeValidator(TestCase):
    """Unit tests for FileSizeValidator."""

    def setUp(self):
        self.validator = FileSizeValidator(max_size_mb=5)

    def test_file_size_validator_valid_file(self):
        """Test file size validator with valid file size."""
        file_content = b"x" * (2 * 1024 * 1024)  # 2MB
        file_obj = SimpleUploadedFile("test.pdf", file_content, content_type="application/pdf")

        # Should not raise any exception
        self.validator(file_obj)

    def test_file_size_validator_file_too_large(self):
        """Test file size validator with file too large."""
        file_content = b"x" * (6 * 1024 * 1024)  # 6MB
        file_obj = SimpleUploadedFile("test.pdf", file_content, content_type="application/pdf")

        with self.assertRaises(ValidationError) as cm:
            self.validator(file_obj)

        self.assertIn("5 MB", str(cm.exception))

    def test_file_size_validator_exact_size(self):
        """Test file size validator with exact size limit."""
        file_content = b"x" * (5 * 1024 * 1024)  # 5MB
        file_obj = SimpleUploadedFile("test.pdf", file_content, content_type="application/pdf")

        # Should not raise any exception
        self.validator(file_obj)

    def test_file_size_validator_no_size_attribute(self):
        """Test file size validator with object without size attribute."""

        class DummyFile:
            pass

        dummy_file = DummyFile()

        # Should not raise any exception
        self.validator(dummy_file)

    def test_file_size_validator_equality(self):
        """Test file size validator equality comparison."""
        validator1 = FileSizeValidator(max_size_mb=5)
        validator2 = FileSizeValidator(max_size_mb=5)
        validator3 = FileSizeValidator(max_size_mb=10)

        self.assertEqual(validator1, validator2)
        self.assertNotEqual(validator1, validator3)

    def test_file_size_validator_different_type(self):
        """Test file size validator equality with different type."""
        validator = FileSizeValidator(max_size_mb=5)
        other_object = "not a validator"

        self.assertNotEqual(validator, other_object)


class TestFileTypeValidator(TestCase):
    """Unit tests for FileTypeValidator."""

    def setUp(self):
        self.validator = FileTypeValidator()

    def test_file_type_validator_valid_pdf(self):
        """Test file type validator with valid PDF file."""
        file_obj = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")

        # Should not raise any exception
        self.validator(file_obj)

    def test_file_type_validator_valid_docx(self):
        """Test file type validator with valid DOCX file."""
        file_obj = SimpleUploadedFile(
            "test.docx",
            b"content",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        # Should not raise any exception
        self.validator(file_obj)

    def test_file_type_validator_invalid_type(self):
        """Test file type validator with invalid file type."""
        file_obj = SimpleUploadedFile("test.txt", b"content", content_type="text/plain")

        with self.assertRaises(ValidationError) as cm:
            self.validator(file_obj)

        self.assertIn("PDF and DOCX", str(cm.exception))

    def test_file_type_validator_no_content_type(self):
        """Test file type validator with object without content_type attribute."""

        class DummyFile:
            pass

        dummy_file = DummyFile()

        # Should not raise any exception
        self.validator(dummy_file)

    def test_file_type_validator_custom_allowed_types(self):
        """Test file type validator with custom allowed types."""
        custom_validator = FileTypeValidator(allowed_types=["image/jpeg", "image/png"])

        # Test with allowed type
        file_obj = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
        custom_validator(file_obj)  # Should not raise

        # Test with disallowed type
        file_obj = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        with self.assertRaises(ValidationError):
            custom_validator(file_obj)

    def test_file_type_validator_equality(self):
        """Test file type validator equality comparison."""
        validator1 = FileTypeValidator()
        validator2 = FileTypeValidator()
        validator3 = FileTypeValidator(allowed_types=["image/jpeg"])

        self.assertEqual(validator1, validator2)
        self.assertNotEqual(validator1, validator3)

    def test_file_type_validator_different_type(self):
        """Test file type validator equality with different type."""
        validator = FileTypeValidator()
        other_object = "not a validator"

        self.assertNotEqual(validator, other_object)


class TestAgeValidator(TestCase):
    """Unit tests for AgeValidator."""

    def setUp(self):
        self.validator = AgeValidator(min_age=16, max_age=100)

    def test_age_validator_valid_age(self):
        """Test age validator with valid age."""
        valid_date = date(1990, 1, 1)  # Age will be calculated based on current date

        # Should not raise any exception
        self.validator(valid_date)

    def test_age_validator_exact_min_age(self):
        """Test age validator with exact minimum age."""
        min_age_date = subtract_years(date.today(), 16)
        self.validator(min_age_date)

    def test_age_validator_too_old(self):
        """Test age validator with too old age."""
        too_old_date = subtract_years(date.today(), 101)
        with self.assertRaises(ValidationError) as cm:
            self.validator(too_old_date)
        self.assertIn("valid date of birth", str(cm.exception))

    def test_phone_number_validator_invalid_numbers(self):
        """Test phone number validator with invalid numbers."""
        phone_validator = PhoneNumberValidator()
        invalid_numbers = [
            "invalid",
            "abc123",
            "",
            None,
        ]
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                phone_validator(number)

    def test_phone_number_validator_edge_cases(self):
        """Test phone number validator edge cases."""
        validator = PhoneNumberValidator()
        # Test with minimum valid length (10 digits, not starting with 0)
        validator("1234567890")  # Should not raise
        # Test with maximum valid length (15 digits, not starting with 0)
        validator("123456789012345")  # Should not raise
        # Test with too short number (less than 10 digits)
        with self.assertRaises(ValidationError):
            validator("123456789")
        # Test with too long number (more than 15 digits)
        with self.assertRaises(ValidationError):
            validator("1234567890123456")

    def test_age_validator_edge_cases(self):
        """Test age validator edge cases."""
        validator = AgeValidator(min_age=18, max_age=65)
        exact_18 = subtract_years(date.today(), 18)
        validator(exact_18)  # Should not raise
        exact_65 = subtract_years(date.today(), 65)
        validator(exact_65)  # Should not raise


class TestExperienceValidator(TestCase):
    """Unit tests for ExperienceValidator."""

    def setUp(self):
        self.validator = ExperienceValidator(min_years=0, max_years=50)

    def test_experience_validator_valid_experience(self):
        """Test experience validator with valid experience."""
        # Should not raise any exception
        self.validator(5)

    def test_experience_validator_too_low(self):
        """Test experience validator with too low experience."""
        with self.assertRaises(ValidationError) as cm:
            self.validator(-1)

        self.assertIn("0", str(cm.exception))

    def test_experience_validator_too_high(self):
        """Test experience validator with too high experience."""
        with self.assertRaises(ValidationError) as cm:
            self.validator(51)

        self.assertIn("50", str(cm.exception))

    def test_experience_validator_exact_min(self):
        """Test experience validator with exact minimum."""
        # Should not raise any exception
        self.validator(0)

    def test_experience_validator_exact_max(self):
        """Test experience validator with exact maximum."""
        # Should not raise any exception
        self.validator(50)

    def test_experience_validator_equality(self):
        """Test experience validator equality comparison."""
        validator1 = ExperienceValidator(min_years=0, max_years=50)
        validator2 = ExperienceValidator(min_years=0, max_years=50)
        validator3 = ExperienceValidator(min_years=1, max_years=50)

        self.assertEqual(validator1, validator2)
        self.assertNotEqual(validator1, validator3)

    def test_experience_validator_different_type(self):
        """Test experience validator equality with different type."""
        validator = ExperienceValidator(min_years=0, max_years=50)
        other_object = "not a validator"

        self.assertNotEqual(validator, other_object)


class TestPhoneNumberValidator(TestCase):
    """Unit tests for PhoneNumberValidator."""

    def setUp(self):
        self.validator = PhoneNumberValidator()

    def test_phone_number_validator_valid_numbers(self):
        """Test phone number validator with valid numbers."""
        valid_numbers = [
            "+1234567890",
            "+123456789012345",
            "1234567890",
            "+12345678901",
        ]
        for number in valid_numbers:
            self.validator(number)

    def test_phone_number_validator_invalid_numbers(self):
        """Test phone number validator with invalid numbers."""
        invalid_numbers = [
            "invalid",
            "abc123",
            "",
            None,
        ]
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                self.validator(number)

    def test_phone_number_validator_empty_string(self):
        """Test phone number validator with empty string."""
        with self.assertRaises(ValidationError):
            self.validator("")

    def test_phone_number_validator_none_value(self):
        """Test phone number validator with None value."""
        with self.assertRaises(ValidationError):
            self.validator(None)

    def test_phone_number_validator_equality(self):
        """Test phone number validator equality comparison."""
        validator1 = PhoneNumberValidator()
        validator2 = PhoneNumberValidator()

        self.assertEqual(validator1, validator2)

    def test_phone_number_validator_different_type(self):
        """Test phone number validator equality with different type."""
        validator = PhoneNumberValidator()
        other_object = "not a validator"

        self.assertNotEqual(validator, other_object)


class TestPreConfiguredValidators(TestCase):
    """Unit tests for pre-configured validators."""

    def test_file_size_validator_instance(self):
        """Test that file_size_validator is properly configured."""
        self.assertIsInstance(file_size_validator, FileSizeValidator)
        self.assertEqual(file_size_validator.max_size_mb, 5)

    def test_file_type_validator_instance(self):
        """Test that file_type_validator is properly configured."""
        self.assertIsInstance(file_type_validator, FileTypeValidator)
        expected_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]
        self.assertEqual(file_type_validator.allowed_types, expected_types)

    def test_age_validator_instance(self):
        """Test that age_validator is properly configured."""
        self.assertIsInstance(age_validator, AgeValidator)
        self.assertEqual(age_validator.min_age, 16)
        self.assertEqual(age_validator.max_age, 100)

    def test_experience_validator_instance(self):
        """Test that experience_validator is properly configured."""
        self.assertIsInstance(experience_validator, ExperienceValidator)
        self.assertEqual(experience_validator.min_years, 0)
        self.assertEqual(experience_validator.max_years, 50)

    def test_phone_number_validator_instance(self):
        """Test that phone_number_validator is properly configured."""
        self.assertIsInstance(phone_number_validator, PhoneNumberValidator)


class TestValidatorDocumentation(TestCase):
    """Test validator documentation and docstrings."""

    def test_file_size_validator_docstring(self):
        """Test that FileSizeValidator has proper documentation."""
        doc = FileSizeValidator.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("file size", doc)

    def test_file_type_validator_docstring(self):
        """Test that FileTypeValidator has proper documentation."""
        doc = FileTypeValidator.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("file type", doc)

    def test_age_validator_docstring(self):
        """Test that AgeValidator has proper documentation."""
        doc = AgeValidator.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("age", doc)

    def test_experience_validator_docstring(self):
        """Test that ExperienceValidator has proper documentation."""
        doc = ExperienceValidator.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("experience", doc)

    def test_phone_number_validator_docstring(self):
        """Test that PhoneNumberValidator has proper documentation."""
        doc = PhoneNumberValidator.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("phone number", doc)


class TestValidatorEdgeCases(TestCase):
    """Test validator edge cases and error handling."""

    def test_file_size_validator_edge_cases(self):
        """Test file size validator edge cases."""
        validator = FileSizeValidator(max_size_mb=1)

        # Test with exactly 1MB
        file_content = b"x" * (1 * 1024 * 1024)
        file_obj = SimpleUploadedFile("test.pdf", file_content, content_type="application/pdf")
        validator(file_obj)  # Should not raise

        # Test with 1MB + 1 byte
        file_content = b"x" * (1 * 1024 * 1024 + 1)
        file_obj = SimpleUploadedFile("test.pdf", file_content, content_type="application/pdf")
        with self.assertRaises(ValidationError):
            validator(file_obj)

    def test_experience_validator_edge_cases(self):
        """Test experience validator edge cases."""
        validator = ExperienceValidator(min_years=1, max_years=30)

        # Test with exactly 1 year
        validator(1)  # Should not raise

        # Test with exactly 30 years
        validator(30)  # Should not raise

        # Test with 0 years (should fail)
        with self.assertRaises(ValidationError):
            validator(0)

        # Test with 31 years (should fail)
        with self.assertRaises(ValidationError):
            validator(31)
