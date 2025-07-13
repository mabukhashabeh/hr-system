from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory
from faker import Faker

from candidate.models import ApplicationStatus, Candidate, Department, StatusHistory

User = get_user_model()


# Test Factories
class UserFactory(DjangoModelFactory):
    """Factory for creating test users."""

    class Meta:
        model = User

    username = FactoryFaker("user_name")
    email = FactoryFaker("email")
    password = FactoryFaker("password")


class CandidateFactory(DjangoModelFactory):
    """Factory for creating test candidates."""

    class Meta:
        model = Candidate

    id = FactoryFaker("uuid4")
    full_name = FactoryFaker("name")
    email = FactoryFaker("email")
    phone = FactoryFaker("numerify", text="+1-###-###-####")
    date_of_birth = FactoryFaker("date_of_birth", minimum_age=18, maximum_age=65)
    years_of_experience = FactoryFaker("random_int", min=0, max=20)
    department = FactoryFaker("random_element", elements=[dept[0] for dept in Department.choices])
    current_status = ApplicationStatus.SUBMITTED

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create candidate with resume file."""
        # Create a dummy resume file
        resume_content = b"Fake resume content"
        resume_file = SimpleUploadedFile("test_resume.pdf", resume_content, content_type="application/pdf")
        kwargs["resume"] = resume_file
        return super()._create(model_class, *args, **kwargs)


class StatusHistoryFactory(DjangoModelFactory):
    """Factory for creating test status history."""

    class Meta:
        model = StatusHistory

    id = FactoryFaker("uuid4")
    candidate = FactoryFaker("sub_factory", factory=CandidateFactory)
    previous_status = None
    new_status = ApplicationStatus.SUBMITTED
    feedback = FactoryFaker("text", max_nb_chars=200)
    admin_name = FactoryFaker("name")
    admin_email = FactoryFaker("email")


# Unit Tests
class TestCandidateModel(TestCase):
    """Unit tests for Candidate model."""

    def setUp(self):
        self.faker = Faker()
        self.candidate_data = {
            "full_name": self.faker.name(),
            "email": self.faker.email(),
            "phone": "+1234567890",
            "date_of_birth": date(1990, 1, 1),
            "years_of_experience": 5,
            "department": Department.IT,
            "current_status": ApplicationStatus.SUBMITTED,
        }

    def test_candidate_creation(self):
        """Test basic candidate creation."""
        resume_file = SimpleUploadedFile("test.pdf", b"test content", content_type="application/pdf")
        self.candidate_data["resume"] = resume_file

        candidate = Candidate.objects.create(**self.candidate_data)

        self.assertIsNotNone(candidate.id)
        self.assertEqual(candidate.full_name, self.candidate_data["full_name"])
        self.assertEqual(candidate.email, self.candidate_data["email"])
        self.assertEqual(candidate.current_status, ApplicationStatus.SUBMITTED)

    def test_candidate_age_calculation(self):
        """Test age calculation property."""
        candidate = CandidateFactory(date_of_birth=date(1990, 1, 1))
        expected_age = date.today().year - 1990
        self.assertEqual(candidate.age, expected_age)

    def test_candidate_age_none(self):
        """Test age calculation when date_of_birth is None."""
        candidate = Candidate()
        candidate.date_of_birth = None
        self.assertIsNone(candidate.age)

    def test_candidate_string_representation(self):
        """Test string representation."""
        candidate = CandidateFactory()
        expected = f"{candidate.full_name} - {candidate.department}"
        self.assertEqual(str(candidate), expected)

    def test_candidate_ordering(self):
        """Test default ordering by created_at descending."""
        candidate1 = CandidateFactory()
        import time

        time.sleep(0.001)  # Small delay to ensure different timestamps
        candidate2 = CandidateFactory()

        candidates = Candidate.objects.all()
        # Compare IDs as strings since UUID comparison can be tricky
        self.assertEqual(str(candidates[0].id), str(candidate2.id))  # Most recent first
        self.assertEqual(str(candidates[1].id), str(candidate1.id))

    def test_unique_email_constraint(self):
        """Test email uniqueness constraint."""
        candidate1 = CandidateFactory()

        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            CandidateFactory(email=candidate1.email)

    def test_unique_phone_constraint(self):
        """Test phone uniqueness constraint."""
        candidate1 = CandidateFactory()

        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            CandidateFactory(phone=candidate1.phone)

    def test_indexes_exist(self):
        """Test that required indexes exist."""
        indexes = [index.name for index in Candidate._meta.indexes]
        # Check that indexes exist (actual names may vary)
        self.assertGreater(len(indexes), 0)
        # Check that we have the expected number of indexes
        self.assertEqual(len(indexes), 2)

    def test_verbose_names(self):
        """Test model verbose names."""
        self.assertEqual(Candidate._meta.verbose_name, "candidate")
        self.assertEqual(Candidate._meta.verbose_name_plural, "candidates")

    def test_database_table_name(self):
        """Test database table name."""
        self.assertEqual(Candidate._meta.db_table, "candidates")


class TestStatusHistoryModel(TestCase):
    """Unit tests for StatusHistory model."""

    def setUp(self):
        self.candidate = CandidateFactory()

    def test_status_history_creation(self):
        """Test basic status history creation."""
        status_history = StatusHistory.objects.create(
            candidate=self.candidate,
            new_status=ApplicationStatus.UNDER_REVIEW,
            feedback="Under review",
            admin_name="Admin User",
            admin_email="admin@example.com",
        )

        self.assertIsNotNone(status_history.id)
        self.assertEqual(status_history.candidate, self.candidate)
        self.assertEqual(status_history.new_status, ApplicationStatus.UNDER_REVIEW)

    def test_status_history_string_representation(self):
        """Test string representation."""
        status_history = StatusHistoryFactory(
            candidate=self.candidate,
            previous_status=ApplicationStatus.SUBMITTED,
            new_status=ApplicationStatus.UNDER_REVIEW,
        )

        expected = f"{self.candidate.full_name}: {ApplicationStatus.SUBMITTED} -> {ApplicationStatus.UNDER_REVIEW}"
        self.assertEqual(str(status_history), expected)

    def test_status_history_ordering(self):
        """Test default ordering by created_at descending."""
        history1 = StatusHistoryFactory(candidate=self.candidate)
        import time

        time.sleep(0.001)  # Small delay to ensure different timestamps
        history2 = StatusHistoryFactory(candidate=self.candidate)

        histories = StatusHistory.objects.filter(candidate=self.candidate)
        # Compare IDs as strings since UUID comparison can be tricky
        self.assertEqual(str(histories[0].id), str(history2.id))  # Most recent first
        self.assertEqual(str(histories[1].id), str(history1.id))

    def test_verbose_names(self):
        """Test model verbose names."""
        self.assertEqual(StatusHistory._meta.verbose_name, "status history")
        # Django's default pluralization may vary
        self.assertIn(StatusHistory._meta.verbose_name_plural, ["status historys", "status histories"])

    def test_database_table_name(self):
        """Test database table name."""
        self.assertEqual(StatusHistory._meta.db_table, "status_history")

    def test_indexes_exist(self):
        """Test that required indexes exist."""
        indexes = [index.name for index in StatusHistory._meta.indexes]
        expected_indexes = ["status_hist_candida_47fe2d_idx"]
        for expected in expected_indexes:
            self.assertIn(expected, indexes)


class TestDepartmentChoices(TestCase):
    """Test Department choices."""

    def test_department_choices_exist(self):
        """Test that all expected department choices exist."""
        expected_choices = [
            ("it", "Information Technology"),
            ("hr", "Human Resources"),
            ("finance", "Finance"),
        ]
        self.assertEqual(Department.choices, expected_choices)

    def test_department_choices_values(self):
        """Test department choice values."""
        self.assertEqual(Department.IT, "it")
        self.assertEqual(Department.HR, "hr")
        self.assertEqual(Department.FINANCE, "finance")


class TestApplicationStatusChoices(TestCase):
    """Test ApplicationStatus choices."""

    def test_application_status_choices_exist(self):
        """Test that all expected application status choices exist."""
        expected_choices = [
            ("submitted", "Submitted"),
            ("under_review", "Under Review"),
            ("interview_scheduled", "Interview Scheduled"),
            ("rejected", "Rejected"),
            ("accepted", "Accepted"),
        ]
        self.assertEqual(ApplicationStatus.choices, expected_choices)

    def test_application_status_choices_values(self):
        """Test application status choice values."""
        self.assertEqual(ApplicationStatus.SUBMITTED, "submitted")
        self.assertEqual(ApplicationStatus.UNDER_REVIEW, "under_review")
        self.assertEqual(ApplicationStatus.INTERVIEW_SCHEDULED, "interview_scheduled")
        self.assertEqual(ApplicationStatus.REJECTED, "rejected")
        self.assertEqual(ApplicationStatus.ACCEPTED, "accepted")
