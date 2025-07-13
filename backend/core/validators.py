from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from typing import Any
import re


@deconstructible
class FileSizeValidator:
    """Validator for file size limits"""
    
    def __init__(self, max_size_mb: int = 5):
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    def __call__(self, value: Any) -> None:
        if hasattr(value, 'size') and value.size > self.max_size_bytes:
            raise ValidationError(f"File size cannot exceed {self.max_size_mb} MB.")
    
    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator) and
            self.max_size_mb == other.max_size_mb
        )


@deconstructible
class FileTypeValidator:
    """Validator for file type restrictions"""
    
    def __init__(self, allowed_types: list[str] = None):
        self.allowed_types = allowed_types or [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
    
    def __call__(self, value: Any) -> None:
        if hasattr(value, 'content_type') and value.content_type not in self.allowed_types:
            raise ValidationError("Only PDF and DOCX files are allowed")
    
    def __eq__(self, other):
        return (
            isinstance(other, FileTypeValidator) and
            self.allowed_types == other.allowed_types
        )


@deconstructible
class AgeValidator:
    """Validator for reasonable age ranges"""
    
    def __init__(self, min_age: int = 16, max_age: int = 100):
        self.min_age = min_age
        self.max_age = max_age
    
    def __call__(self, value: Any) -> None:
        if not value:
            return
        
        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < self.min_age:  # pragma: no cover
            raise ValidationError(f"Candidate must be at least {self.min_age} years old.")
        if age > self.max_age:
            raise ValidationError("Please provide a valid date of birth.")
    
    def __eq__(self, other):
        return (
            isinstance(other, AgeValidator) and
            self.min_age == other.min_age and
            self.max_age == other.max_age
        )


@deconstructible
class ExperienceValidator:
    """Validator for years of experience"""
    
    def __init__(self, min_years: int = 0, max_years: int = 50):
        self.min_years = min_years
        self.max_years = max_years
    
    def __call__(self, value: Any) -> None:
        if value < self.min_years:
            raise ValidationError(f"Years of experience cannot be less than {self.min_years}.")
        if value > self.max_years:
            raise ValidationError(f"Years of experience cannot exceed {self.max_years}.")
    
    def __eq__(self, other):
        return (
            isinstance(other, ExperienceValidator) and
            self.min_years == other.min_years and
            self.max_years == other.max_years
        )


@deconstructible
class PhoneNumberValidator:
    """Validator for phone number format"""

    def __call__(self, value: Any) -> None:
        if not value or not isinstance(value, str):
            raise ValidationError("Phone number must be a valid string.")

        # Simple regex for phone number validation (can be extended)
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise ValidationError("Invalid phone number format. Use E.164 format.")
    
    def __eq__(self, other):
        return isinstance(other, PhoneNumberValidator)


# Pre-configured validators
file_size_validator = FileSizeValidator(max_size_mb=5)
file_type_validator = FileTypeValidator()
age_validator = AgeValidator(min_age=16, max_age=100)
experience_validator = ExperienceValidator(min_years=0, max_years=50)
phone_number_validator = PhoneNumberValidator()