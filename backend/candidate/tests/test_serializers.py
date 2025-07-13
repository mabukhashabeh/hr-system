from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import Faker

from candidate.models import ApplicationStatus, Department, StatusHistory
from candidate.serializers import (
    CandidateListSerializer,
    CandidateRegistrationSerializer,
    CandidateStatusSerializer,
    StatusUpdateSerializer,
)


class TestCandidateSerializer(TestCase):
    """Unit tests for candidate serializers."""

    def setUp(self):
        self.faker = Faker()
        self.candidate_data = {
            "full_name": self.faker.name(),
            "email": self.faker.email(),
            "phone": "+1234567890",
            "date_of_birth": date(1990, 1, 1),
            "years_of_experience": 5,
            "department": Department.IT,
        }

    def test_candidate_registration_serializer_valid_data(self):
        """Test registration serializer with valid data."""
        resume_file = SimpleUploadedFile("test.pdf", b"test content", content_type="application/pdf")
        data = {**self.candidate_data, "resume": resume_file}

        serializer = CandidateRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        candidate = serializer.save()
        self.assertEqual(candidate.full_name, self.candidate_data["full_name"])
        self.assertEqual(candidate.current_status, ApplicationStatus.SUBMITTED)

        # Check that status history was created
        self.assertTrue(StatusHistory.objects.filter(candidate=candidate).exists())

    def test_candidate_registration_serializer_invalid_email(self):
        """Test registration serializer with invalid email."""
        data = {**self.candidate_data, "email": "invalid-email"}
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_candidate_registration_serializer_invalid_phone(self):
        """Test registration serializer with invalid phone."""
        data = {**self.candidate_data, "phone": "invalid-phone"}
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_candidate_registration_serializer_invalid_age(self):
        """Test registration serializer with invalid age (too young)."""
        data = {**self.candidate_data, "date_of_birth": date.today()}
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("date_of_birth", serializer.errors)

    def test_candidate_registration_serializer_invalid_experience(self):
        """Test registration serializer with invalid experience."""
        data = {**self.candidate_data, "years_of_experience": 55}  # Too high (over 50)
        data["resume"] = SimpleUploadedFile("test.pdf", b"test content", content_type="application/pdf")
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("years_of_experience", serializer.errors)

    def test_candidate_registration_serializer_get_age(self):
        """Test get_age method in registration serializer."""

        class Dummy:
            age = 42

        serializer = CandidateRegistrationSerializer()
        self.assertEqual(serializer.get_age(Dummy()), 42)

    def test_candidate_list_serializer_get_age(self):
        """Test get_age method in list serializer."""

        class Dummy:
            age = 24

        serializer = CandidateListSerializer()
        self.assertEqual(serializer.get_age(Dummy()), 24)

    def test_status_update_serializer_valid_transition(self):
        """Test status update serializer with valid transition."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory(current_status=ApplicationStatus.SUBMITTED)

        data = {
            "new_status": ApplicationStatus.UNDER_REVIEW,
            "feedback": "Moving to review phase",
            "admin_name": "Admin User",
            "admin_email": "admin@example.com",
        }

        serializer = StatusUpdateSerializer(data=data, context={"candidate": candidate})
        self.assertTrue(serializer.is_valid())

    def test_status_update_serializer_invalid_transition(self):
        """Test status update serializer with invalid transition."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory(current_status=ApplicationStatus.SUBMITTED)

        data = {
            "new_status": ApplicationStatus.ACCEPTED,  # Invalid transition
            "feedback": "Invalid transition",
            "admin_name": "Admin User",
            "admin_email": "admin@example.com",
        }

        serializer = StatusUpdateSerializer(data=data, context={"candidate": candidate})
        self.assertFalse(serializer.is_valid())
        self.assertIn("new_status", serializer.errors)

    def test_status_update_serializer_validate_new_status_no_candidate(self):
        """Test validate_new_status when no candidate in context."""
        serializer = StatusUpdateSerializer(context={})
        self.assertEqual(serializer.validate_new_status("any"), "any")

    def test_candidate_status_serializer_valid_email(self):
        """Test status serializer with valid email."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()

        data = {"email": candidate.email}
        serializer = CandidateStatusSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_candidate_status_serializer_invalid_email(self):
        """Test status serializer with invalid email."""
        data = {"email": "nonexistent@example.com"}
        serializer = CandidateStatusSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
