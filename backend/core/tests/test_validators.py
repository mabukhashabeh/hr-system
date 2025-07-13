import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta


class TestValidators(TestCase):
    """Unit tests for core validators."""
    
    def test_file_size_validator_too_large(self):
        """Test FileSizeValidator with file too large."""
        from core.validators import FileSizeValidator
        
        class Dummy:
            size = 6 * 1024 * 1024
        
        validator = FileSizeValidator(max_size_mb=5)
        with pytest.raises(ValidationError):
            validator(Dummy())
    
    def test_file_size_validator_eq(self):
        """Test FileSizeValidator equality."""
        from core.validators import FileSizeValidator
        
        self.assertEqual(FileSizeValidator(5), FileSizeValidator(5))
        self.assertNotEqual(FileSizeValidator(5), FileSizeValidator(10))
    
    def test_file_type_validator_not_allowed(self):
        """Test FileTypeValidator with disallowed file type."""
        from core.validators import FileTypeValidator
        
        class Dummy:
            content_type = 'application/zip'
        
        validator = FileTypeValidator()
        with pytest.raises(ValidationError):
            validator(Dummy())
    
    def test_file_type_validator_eq(self):
        """Test FileTypeValidator equality."""
        from core.validators import FileTypeValidator
        
        self.assertEqual(FileTypeValidator(['application/pdf']), FileTypeValidator(['application/pdf']))
        self.assertNotEqual(FileTypeValidator(['application/pdf']), FileTypeValidator(['application/zip']))
    
    def test_age_validator_too_young(self):
        """Test AgeValidator with age too young."""
        from core.validators import AgeValidator
        
        validator = AgeValidator(min_age=16, max_age=100)
        too_young = date.today() - timedelta(days=365*10)
        with pytest.raises(ValidationError):
            validator(too_young)
    
    def test_age_validator_too_old(self):
        """Test AgeValidator with age too old."""
        from core.validators import AgeValidator
        
        validator = AgeValidator(min_age=16, max_age=100)
        too_old = date.today() - timedelta(days=365*120)
        with pytest.raises(ValidationError):
            validator(too_old)
    
    def test_age_validator_eq(self):
        """Test AgeValidator equality."""
        from core.validators import AgeValidator
        
        self.assertEqual(AgeValidator(16, 100), AgeValidator(16, 100))
        self.assertNotEqual(AgeValidator(16, 100), AgeValidator(18, 100))
    
    def test_experience_validator_too_little(self):
        """Test ExperienceValidator with too little experience."""
        from core.validators import ExperienceValidator
        
        validator = ExperienceValidator(min_years=0, max_years=50)
        with pytest.raises(ValidationError):
            validator(-1)
    
    def test_experience_validator_too_much(self):
        """Test ExperienceValidator with too much experience."""
        from core.validators import ExperienceValidator
        
        validator = ExperienceValidator(min_years=0, max_years=50)
        with pytest.raises(ValidationError):
            validator(100)
    
    def test_experience_validator_eq(self):
        """Test ExperienceValidator equality."""
        from core.validators import ExperienceValidator
        
        self.assertEqual(ExperienceValidator(0, 50), ExperienceValidator(0, 50))
        self.assertNotEqual(ExperienceValidator(0, 50), ExperienceValidator(1, 50))
    
    def test_phone_number_validator_not_string(self):
        """Test PhoneNumberValidator with non-string value."""
        from core.validators import PhoneNumberValidator
        
        validator = PhoneNumberValidator()
        with pytest.raises(ValidationError):
            validator(123456)
    
    def test_phone_number_validator_invalid_format(self):
        """Test PhoneNumberValidator with invalid format."""
        from core.validators import PhoneNumberValidator
        
        validator = PhoneNumberValidator()
        with pytest.raises(ValidationError):
            validator('notaphone')
    
    def test_phone_number_validator_eq(self):
        """Test PhoneNumberValidator equality."""
        from core.validators import PhoneNumberValidator
        
        self.assertEqual(PhoneNumberValidator(), PhoneNumberValidator())
        self.assertNotEqual(PhoneNumberValidator(), object()) 