import pytest
import tempfile
import os
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from faker import Faker
from factory import Faker as FactoryFaker
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute
from PIL import Image
import io

from candidate.models import Candidate, StatusHistory, Department, ApplicationStatus
from candidate.serializers import (
    CandidateRegistrationSerializer,
    StatusUpdateSerializer,
    CandidateStatusSerializer
)
from candidate.views import CandidateViewSet, StatusHistoryViewSet
from candidate.permissions import CandidatePermission, AdminOnlyPermission


# Test Factories
class CandidateFactory(DjangoModelFactory):
    """Factory for creating test candidates."""
    
    class Meta:
        model = Candidate
    
    id = FactoryFaker('uuid4')
    full_name = FactoryFaker('name')
    email = FactoryFaker('email')
    phone = FactoryFaker('phone_number')
    date_of_birth = FactoryFaker('date_of_birth', minimum_age=18, maximum_age=65)
    years_of_experience = FactoryFaker('random_int', min=0, max=20)
    department = FactoryFaker('random_element', elements=[dept[0] for dept in Department.choices])
    current_status = ApplicationStatus.SUBMITTED
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create candidate with resume file."""
        # Create a dummy resume file
        resume_content = b"Fake resume content"
        resume_file = SimpleUploadedFile(
            "test_resume.pdf",
            resume_content,
            content_type="application/pdf"
        )
        kwargs['resume'] = resume_file
        return super()._create(model_class, *args, **kwargs)


class StatusHistoryFactory(DjangoModelFactory):
    """Factory for creating test status history."""
    
    class Meta:
        model = StatusHistory
    
    id = FactoryFaker('uuid4')
    candidate = SubFactory(CandidateFactory)
    previous_status = None
    new_status = ApplicationStatus.SUBMITTED
    feedback = FactoryFaker('text', max_nb_chars=200)
    admin_name = FactoryFaker('name')
    admin_email = FactoryFaker('email')


class UserFactory(DjangoModelFactory):
    """Factory for creating test users."""
    
    class Meta:
        model = User
    
    username = FactoryFaker('user_name')
    email = FactoryFaker('email')
    password = FactoryFaker('password')


# Unit Tests
class CandidateModelTest(TestCase):
    """Unit tests for Candidate model."""
    
    def setUp(self):
        self.faker = Faker()
        self.candidate_data = {
            'full_name': self.faker.name(),
            'email': self.faker.email(),
            'phone': '+1234567890',
            'date_of_birth': date(1990, 1, 1),
            'years_of_experience': 5,
            'department': Department.IT,
            'current_status': ApplicationStatus.SUBMITTED,
        }
    
    def test_candidate_creation(self):
        """Test basic candidate creation."""
        resume_file = SimpleUploadedFile(
            "test.pdf",
            b"test content",
            content_type="application/pdf"
        )
        self.candidate_data['resume'] = resume_file
        
        candidate = Candidate.objects.create(**self.candidate_data)
        
        self.assertIsNotNone(candidate.id)
        self.assertEqual(candidate.full_name, self.candidate_data['full_name'])
        self.assertEqual(candidate.email, self.candidate_data['email'])
        self.assertEqual(candidate.current_status, ApplicationStatus.SUBMITTED)
    
    def test_candidate_age_calculation(self):
        """Test age calculation property."""
        candidate = CandidateFactory(date_of_birth=date(1990, 1, 1))
        expected_age = date.today().year - 1990
        self.assertEqual(candidate.age, expected_age)
    
    def test_candidate_string_representation(self):
        """Test string representation."""
        candidate = CandidateFactory()
        expected = f"{candidate.full_name} - {candidate.department}"
        self.assertEqual(str(candidate), expected)
    
    def test_candidate_ordering(self):
        """Test default ordering by created_at descending."""
        candidate1 = CandidateFactory()
        candidate2 = CandidateFactory()
        
        candidates = Candidate.objects.all()
        self.assertEqual(candidates[0], candidate2)  # Most recent first
        self.assertEqual(candidates[1], candidate1)
    
    def test_unique_email_constraint(self):
        """Test email uniqueness constraint."""
        candidate1 = CandidateFactory()
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            CandidateFactory(email=candidate1.email)
    
    def test_unique_phone_constraint(self):
        """Test phone uniqueness constraint."""
        candidate1 = CandidateFactory()
        
        with self.assertRaises(Exception):  # Should raise IntegrityError
            CandidateFactory(phone=candidate1.phone)


class StatusHistoryModelTest(TestCase):
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
            admin_email="admin@example.com"
        )
        
        self.assertIsNotNone(status_history.id)
        self.assertEqual(status_history.candidate, self.candidate)
        self.assertEqual(status_history.new_status, ApplicationStatus.UNDER_REVIEW)
    
    def test_status_history_string_representation(self):
        """Test string representation."""
        status_history = StatusHistoryFactory(
            candidate=self.candidate,
            previous_status=ApplicationStatus.SUBMITTED,
            new_status=ApplicationStatus.UNDER_REVIEW
        )
        
        expected = f"{self.candidate.full_name}: {ApplicationStatus.SUBMITTED} -> {ApplicationStatus.UNDER_REVIEW}"
        self.assertEqual(str(status_history), expected)
    
    def test_status_history_ordering(self):
        """Test default ordering by created_at descending."""
        history1 = StatusHistoryFactory(candidate=self.candidate)
        history2 = StatusHistoryFactory(candidate=self.candidate)
        
        histories = StatusHistory.objects.filter(candidate=self.candidate)
        self.assertEqual(histories[0], history2)  # Most recent first
        self.assertEqual(histories[1], history1)


class CandidateSerializerTest(TestCase):
    """Unit tests for candidate serializers."""
    
    def setUp(self):
        self.faker = Faker()
        self.candidate_data = {
            'full_name': self.faker.name(),
            'email': self.faker.email(),
            'phone': '+1234567890',
            'date_of_birth': date(1990, 1, 1),
            'years_of_experience': 5,
            'department': Department.IT,
        }
    
    def test_candidate_registration_serializer_valid_data(self):
        """Test registration serializer with valid data."""
        resume_file = SimpleUploadedFile(
            "test.pdf",
            b"test content",
            content_type="application/pdf"
        )
        data = {**self.candidate_data, 'resume': resume_file}
        
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        candidate = serializer.save()
        self.assertEqual(candidate.full_name, self.candidate_data['full_name'])
        self.assertEqual(candidate.current_status, ApplicationStatus.SUBMITTED)
        
        # Check that status history was created
        self.assertTrue(StatusHistory.objects.filter(candidate=candidate).exists())
    
    def test_candidate_registration_serializer_invalid_email(self):
        """Test registration serializer with invalid email."""
        data = {**self.candidate_data, 'email': 'invalid-email'}
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_candidate_registration_serializer_invalid_phone(self):
        """Test registration serializer with invalid phone."""
        data = {**self.candidate_data, 'phone': 'invalid-phone'}
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone', serializer.errors)
    
    def test_candidate_registration_serializer_invalid_age(self):
        """Test registration serializer with invalid age (too young)."""
        data = {**self.candidate_data, 'date_of_birth': date.today()}
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_of_birth', serializer.errors)
    
    def test_candidate_registration_serializer_invalid_experience(self):
        """Test registration serializer with invalid experience."""
        data = {**self.candidate_data, 'years_of_experience': 25}  # Too high
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('years_of_experience', serializer.errors)
    
    def test_status_update_serializer_valid_transition(self):
        """Test status update serializer with valid transition."""
        candidate = CandidateFactory(current_status=ApplicationStatus.SUBMITTED)
        
        data = {
            'new_status': ApplicationStatus.UNDER_REVIEW,
            'feedback': 'Moving to review phase',
            'admin_name': 'Admin User',
            'admin_email': 'admin@example.com'
        }
        
        serializer = StatusUpdateSerializer(
            data=data,
            context={'candidate': candidate}
        )
        self.assertTrue(serializer.is_valid())
    
    def test_status_update_serializer_invalid_transition(self):
        """Test status update serializer with invalid transition."""
        candidate = CandidateFactory(current_status=ApplicationStatus.SUBMITTED)
        
        data = {
            'new_status': ApplicationStatus.ACCEPTED,  # Invalid transition
            'feedback': 'Invalid transition',
            'admin_name': 'Admin User',
            'admin_email': 'admin@example.com'
        }
        
        serializer = StatusUpdateSerializer(
            data=data,
            context={'candidate': candidate}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_status', serializer.errors)
    
    def test_candidate_status_serializer_valid_email(self):
        """Test status serializer with valid email."""
        candidate = CandidateFactory()
        
        data = {'email': candidate.email}
        serializer = CandidateStatusSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_candidate_status_serializer_invalid_email(self):
        """Test status serializer with invalid email."""
        data = {'email': 'nonexistent@example.com'}
        serializer = CandidateStatusSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


# Integration Tests
class CandidateAPITest(APITestCase):
    """Integration tests for candidate API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.faker = Faker()
        
        # Create test user for admin operations
        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()
        
        # Create test candidates
        self.candidate1 = CandidateFactory()
        self.candidate2 = CandidateFactory()
    
    def test_candidate_registration_success(self):
        """Test successful candidate registration."""
        data = {
            'full_name': self.faker.name(),
            'email': self.faker.email(),
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'years_of_experience': 5,
            'department': Department.IT,
            'resume': SimpleUploadedFile(
                "test.pdf",
                b"test content",
                content_type="application/pdf"
            )
        }
        
        response = self.client.post('/api/candidates/', data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['full_name'], data['full_name'])
        self.assertEqual(response.data['current_status'], ApplicationStatus.SUBMITTED)
    
    def test_candidate_registration_invalid_data(self):
        """Test candidate registration with invalid data."""
        data = {
            'full_name': self.faker.name(),
            'email': 'invalid-email',
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'years_of_experience': 5,
            'department': Department.IT,
        }
        
        response = self.client.post('/api/candidates/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_candidate_list_admin_access(self):
        """Test candidate list endpoint with admin access."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get('/api/candidates/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_candidate_list_unauthorized_access(self):
        """Test candidate list endpoint without admin access."""
        response = self.client.get('/api/candidates/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_candidate_detail_admin_access(self):
        """Test candidate detail endpoint with admin access."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get(f'/api/candidates/{self.candidate1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.candidate1.id))
        self.assertEqual(response.data['full_name'], self.candidate1.full_name)
    
    def test_candidate_status_check_public_access(self):
        """Test candidate status check with public access."""
        response = self.client.get(
            '/api/candidates/status/',
            {'email': self.candidate1.email}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.candidate1.email)
        self.assertEqual(response.data['current_status'], self.candidate1.current_status)
    
    def test_candidate_status_check_invalid_email(self):
        """Test candidate status check with invalid email."""
        response = self.client.get(
            '/api/candidates/status/',
            {'email': 'nonexistent@example.com'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_candidate_status_update_admin_access(self):
        """Test candidate status update with admin access."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'new_status': ApplicationStatus.UNDER_REVIEW,
            'feedback': 'Moving to review phase',
            'admin_name': 'Admin User',
            'admin_email': 'admin@example.com'
        }
        
        response = self.client.patch(
            f'/api/candidates/{self.candidate1.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_status'], ApplicationStatus.UNDER_REVIEW)
        
        # Check that status history was created
        self.candidate1.refresh_from_db()
        self.assertTrue(
            StatusHistory.objects.filter(
                candidate=self.candidate1,
                new_status=ApplicationStatus.UNDER_REVIEW
            ).exists()
        )
    
    def test_candidate_status_update_invalid_transition(self):
        """Test candidate status update with invalid transition."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'new_status': ApplicationStatus.ACCEPTED,  # Invalid transition
            'feedback': 'Invalid transition',
            'admin_name': 'Admin User',
            'admin_email': 'admin@example.com'
        }
        
        response = self.client.patch(
            f'/api/candidates/{self.candidate1.id}/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_status', response.data)
    
    def test_candidate_filtering_by_status(self):
        """Test candidate filtering by status."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Update one candidate status
        self.candidate1.current_status = ApplicationStatus.UNDER_REVIEW
        self.candidate1.save()
        
        response = self.client.get('/api/candidates/?status=under_review')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], str(self.candidate1.id))
    
    def test_candidate_filtering_by_department(self):
        """Test candidate filtering by department."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get(f'/api/candidates/?department={self.candidate1.department}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return candidates with matching department
        for result in response.data['results']:
            self.assertEqual(result['department'], self.candidate1.get_department_display())
    
    def test_candidate_search_by_name(self):
        """Test candidate search by name."""
        self.client.force_authenticate(user=self.admin_user)
        
        search_name = self.candidate1.full_name.split()[0]  # First name
        response = self.client.get(f'/api/candidates/?search={search_name}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_candidate_search_by_email(self):
        """Test candidate search by email."""
        self.client.force_authenticate(user=self.admin_user)
        
        search_email = self.candidate1.email.split('@')[0]  # Email prefix
        response = self.client.get(f'/api/candidates/?search={search_email}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_candidate_ordering(self):
        """Test candidate ordering."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get('/api/candidates/?ordering=full_name')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        
        # Check if results are ordered by name
        names = [result['full_name'] for result in results]
        self.assertEqual(names, sorted(names))
    
    def test_resume_download_admin_access(self):
        """Test resume download with admin access."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get(f'/api/candidates/{self.candidate1.id}/resume/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('download_url', response.data)
    
    def test_resume_download_unauthorized_access(self):
        """Test resume download without admin access."""
        response = self.client.get(f'/api/candidates/{self.candidate1.id}/resume/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StatusHistoryAPITest(APITestCase):
    """Integration tests for status history API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()
        
        self.candidate = CandidateFactory()
        self.status_history1 = StatusHistoryFactory(candidate=self.candidate)
        self.status_history2 = StatusHistoryFactory(candidate=self.candidate)
    
    def test_status_history_list_admin_access(self):
        """Test status history list with admin access."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get('/api/status-history/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_status_history_list_unauthorized_access(self):
        """Test status history list without admin access."""
        response = self.client.get('/api/status-history/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_status_history_filtering_by_candidate(self):
        """Test status history filtering by candidate."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.get(f'/api/status-history/?candidate={self.candidate.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data['results']:
            self.assertEqual(result['candidate'], self.candidate.id)
    
    def test_status_history_filtering_by_status(self):
        """Test status history filtering by status."""
        self.client.force_authenticate(user=self.admin_user)
        
        status_value = self.status_history1.new_status
        response = self.client.get(f'/api/status-history/?new_status={status_value}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for result in response.data['results']:
            self.assertEqual(result['new_status'], status_value)


class PermissionTest(TestCase):
    """Unit tests for custom permissions."""
    
    def setUp(self):
        self.candidate_permission = CandidatePermission()
        self.admin_permission = AdminOnlyPermission()
        self.user = UserFactory()
        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()
    
    def test_candidate_permission_allow_get(self):
        """Test candidate permission allows GET requests."""
        request = MagicMock()
        request.method = 'GET'
        
        has_permission = self.candidate_permission.has_permission(request, None)
        self.assertTrue(has_permission)
    
    def test_candidate_permission_allow_post(self):
        """Test candidate permission allows POST requests."""
        request = MagicMock()
        request.method = 'POST'
        
        has_permission = self.candidate_permission.has_permission(request, None)
        self.assertTrue(has_permission)
    
    def test_admin_permission_deny_anonymous(self):
        """Test admin permission denies anonymous users."""
        request = MagicMock()
        request.user.is_authenticated = False
        
        has_permission = self.admin_permission.has_permission(request, None)
        self.assertFalse(has_permission)
    
    def test_admin_permission_allow_staff(self):
        """Test admin permission allows staff users."""
        request = MagicMock()
        request.user = self.admin_user
        request.user.is_authenticated = True
        
        has_permission = self.admin_permission.has_permission(request, None)
        self.assertTrue(has_permission)


# Performance Tests
class PerformanceTest(TestCase):
    """Performance tests for candidate operations."""
    
    def setUp(self):
        # Create multiple candidates for performance testing
        self.candidates = [CandidateFactory() for _ in range(50)]
        self.status_histories = [
            StatusHistoryFactory(candidate=candidate) 
            for candidate in self.candidates[:10]
        ]
    
    def test_candidate_list_performance(self):
        """Test candidate list query performance."""
        import time
        
        start_time = time.time()
        candidates = Candidate.objects.all()
        list(candidates)  # Force evaluation
        end_time = time.time()
        
        # Should complete within reasonable time (adjust threshold as needed)
        self.assertLess(end_time - start_time, 1.0)
    
    def test_candidate_filtering_performance(self):
        """Test candidate filtering performance."""
        import time
        
        start_time = time.time()
        candidates = Candidate.objects.filter(department=Department.IT)
        list(candidates)
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 0.5)
    
    def test_status_history_performance(self):
        """Test status history query performance."""
        import time
        
        start_time = time.time()
        histories = StatusHistory.objects.select_related('candidate').all()
        list(histories)
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 0.5)


# Edge Case Tests
class EdgeCaseTest(TestCase):
    """Tests for edge cases and error conditions."""
    
    def test_candidate_without_resume(self):
        """Test candidate creation without resume."""
        candidate_data = {
            'full_name': 'Test Candidate',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'date_of_birth': date(1990, 1, 1),
            'years_of_experience': 5,
            'department': Department.IT,
        }
        
        with self.assertRaises(Exception):
            Candidate.objects.create(**candidate_data)
    
    def test_duplicate_email_registration(self):
        """Test registration with duplicate email."""
        candidate1 = CandidateFactory()
        
        data = {
            'full_name': 'Another Candidate',
            'email': candidate1.email,  # Duplicate email
            'phone': '+1234567891',
            'date_of_birth': '1990-01-01',
            'years_of_experience': 5,
            'department': Department.IT,
            'resume': SimpleUploadedFile(
                "test.pdf",
                b"test content",
                content_type="application/pdf"
            )
        }
        
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_invalid_file_type(self):
        """Test registration with invalid file type."""
        data = {
            'full_name': 'Test Candidate',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'years_of_experience': 5,
            'department': Department.IT,
            'resume': SimpleUploadedFile(
                "test.txt",
                b"test content",
                content_type="text/plain"
            )
        }
        
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('resume', serializer.errors)
    
    def test_large_file_size(self):
        """Test registration with file too large."""
        large_content = b"x" * (10 * 1024 * 1024)  # 10MB
        
        data = {
            'full_name': 'Test Candidate',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'date_of_birth': '1990-01-01',
            'years_of_experience': 5,
            'department': Department.IT,
            'resume': SimpleUploadedFile(
                "test.pdf",
                large_content,
                content_type="application/pdf"
            )
        }
        
        serializer = CandidateRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('resume', serializer.errors)


# Test Configuration
@pytest.mark.django_db
class TestWithDatabase:
    """Pytest-style tests with database access."""
    
    def test_candidate_creation_with_factory(self):
        """Test candidate creation using factory."""
        candidate = CandidateFactory()
        assert candidate.id is not None
        assert candidate.full_name is not None
        assert candidate.email is not None
    
    def test_status_history_creation_with_factory(self):
        """Test status history creation using factory."""
        history = StatusHistoryFactory()
        assert history.id is not None
        assert history.candidate is not None
        assert history.new_status is not None
    
    def test_multiple_candidates_performance(self):
        """Test creating multiple candidates efficiently."""
        candidates = [CandidateFactory() for _ in range(10)]
        assert len(candidates) == 10
        assert all(c.id is not None for c in candidates)


# Test Utilities
class TestUtils:
    """Utility functions for testing."""
    
    @staticmethod
    def create_test_resume_file(filename="test_resume.pdf", content=b"test content"):
        """Create a test resume file."""
        return SimpleUploadedFile(
            filename,
            content,
            content_type="application/pdf"
        )
    
    @staticmethod
    def create_test_image_file(filename="test_image.jpg"):
        """Create a test image file."""
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        return SimpleUploadedFile(
            filename,
            image_io.getvalue(),
            content_type="image/jpeg"
        )
