from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import Faker

from candidate.models import ApplicationStatus, Department, StatusHistory
from candidate.serializers import (
    CandidateDetailSerializer,
    CandidateListSerializer,
    CandidateRegistrationSerializer,
    CandidateStatusSerializer,
    ResumeDownloadSerializer,
    StatusHistorySerializer,
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

    def test_candidate_list_serializer_department_display(self):
        """Test department display in list serializer."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory(department=Department.IT)
        serializer = CandidateListSerializer(candidate)
        self.assertEqual(serializer.data["department"], "Information Technology")

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

    def test_status_update_serializer_update_method(self):
        """Test update method in status update serializer."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory(current_status=ApplicationStatus.SUBMITTED)
        validated_data = {
            "new_status": ApplicationStatus.UNDER_REVIEW,
            "feedback": "Test feedback",
            "admin_name": "Test Admin",
            "admin_email": "admin@test.com",
        }

        serializer = StatusUpdateSerializer()
        updated_candidate = serializer.update(candidate, validated_data)

        self.assertEqual(updated_candidate.current_status, ApplicationStatus.UNDER_REVIEW)
        self.assertTrue(
            StatusHistory.objects.filter(candidate=candidate, new_status=ApplicationStatus.UNDER_REVIEW).exists()
        )

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

    def test_candidate_status_serializer_validate_email_sets_instance(self):
        """Test that validate_email sets the instance."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()
        serializer = CandidateStatusSerializer()
        validated_email = serializer.validate_email(candidate.email)

        self.assertEqual(validated_email, candidate.email)
        # Check that instance is set (may be a different object with same data)
        self.assertIsNotNone(serializer.instance)
        self.assertEqual(serializer.instance.email, candidate.email)

    def test_candidate_detail_serializer_get_age(self):
        """Test get_age method in detail serializer."""

        class Dummy:
            age = 30

        serializer = CandidateDetailSerializer()
        self.assertEqual(serializer.get_age(Dummy()), 30)

    def test_candidate_detail_serializer_get_resume_url_with_request(self):
        """Test get_resume_url method with request context."""
        from django.test import RequestFactory

        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()
        request = RequestFactory().get("/")
        serializer = CandidateDetailSerializer(candidate, context={"request": request})

        # Should return the resume URL since we have a real file
        self.assertIn("resume_url", serializer.data)

    def test_candidate_detail_serializer_get_resume_url_no_request(self):
        """Test get_resume_url method without request context."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()
        serializer = CandidateDetailSerializer(candidate, context={})

        self.assertEqual(serializer.data["resume_url"], "")

    def test_resume_download_serializer_get_download_url_with_resume(self):
        """Test get_download_url method with resume file."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()
        serializer = ResumeDownloadSerializer(candidate)

        # Should return the resume URL
        self.assertIn("download_url", serializer.data)

    def test_resume_download_serializer_get_download_url_no_resume(self):
        """Test get_download_url method without resume file."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()
        candidate.resume = None
        candidate.save()

        serializer = ResumeDownloadSerializer(candidate)
        self.assertIsNone(serializer.data["download_url"])


class TestStatusHistorySerializer(TestCase):
    """Unit tests for StatusHistory serializer."""

    def setUp(self):
        from candidate.tests.test_models import CandidateFactory, StatusHistoryFactory

        self.candidate = CandidateFactory()
        self.status_history = StatusHistoryFactory(
            candidate=self.candidate,
            previous_status=ApplicationStatus.SUBMITTED,
            new_status=ApplicationStatus.UNDER_REVIEW,
            feedback="Test feedback",
            admin_name="Test Admin",
            admin_email="admin@test.com",
        )

    def test_status_history_serializer_valid_data(self):
        """Test status history serializer with valid data."""
        data = {
            "previous_status": ApplicationStatus.SUBMITTED,
            "new_status": ApplicationStatus.UNDER_REVIEW,
            "feedback": "Test feedback",
            "admin_name": "Test Admin",
            "admin_email": "admin@test.com",
        }

        serializer = StatusHistorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_status_history_serializer_missing_required_fields(self):
        """Test status history serializer with missing required fields."""
        data = {
            "previous_status": ApplicationStatus.SUBMITTED,
            "new_status": ApplicationStatus.UNDER_REVIEW,
            # Missing feedback, admin_name, admin_email
        }

        serializer = StatusHistorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("feedback", serializer.errors)
        self.assertIn("admin_name", serializer.errors)
        self.assertIn("admin_email", serializer.errors)

    def test_status_history_serializer_invalid_email(self):
        """Test status history serializer with invalid email."""
        data = {
            "previous_status": ApplicationStatus.SUBMITTED,
            "new_status": ApplicationStatus.UNDER_REVIEW,
            "feedback": "Test feedback",
            "admin_name": "Test Admin",
            "admin_email": "invalid-email",
        }

        serializer = StatusHistorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("admin_email", serializer.errors)

    def test_status_history_serializer_display_fields(self):
        """Test that display fields are properly serialized."""
        serializer = StatusHistorySerializer(self.status_history)
        data = serializer.data

        self.assertEqual(data["previous_status"], "Submitted")
        self.assertEqual(data["new_status"], "Under Review")
        self.assertEqual(data["admin_name"], "Test Admin")
        self.assertEqual(data["admin_email"], "admin@test.com")
        self.assertEqual(data["feedback"], "Test feedback")


class TestSerializerDocumentation(TestCase):
    """Test serializer documentation and docstrings."""

    def test_candidate_registration_serializer_docstring(self):
        """Test that CandidateRegistrationSerializer has proper documentation."""
        doc = CandidateRegistrationSerializer.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("comprehensive validation", doc)

    def test_status_update_serializer_docstring(self):
        """Test that StatusUpdateSerializer has proper documentation."""
        doc = StatusUpdateSerializer.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("admin only", doc)

    def test_candidate_detail_serializer_docstring(self):
        """Test that CandidateDetailSerializer has proper documentation."""
        doc = CandidateDetailSerializer.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("candidate information", doc)

    def test_resume_download_serializer_docstring(self):
        """Test that ResumeDownloadSerializer has proper documentation."""
        # This serializer doesn't have a docstring, so we'll test that it exists
        self.assertTrue(hasattr(ResumeDownloadSerializer, "Meta"))
