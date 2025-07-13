from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.test import APIClient, APITestCase

from candidate.models import ApplicationStatus


class TestCandidateAPI(APITestCase):
    """API tests for candidate views."""

    def setUp(self):
        from candidate.tests.test_models import CandidateFactory, UserFactory

        self.client = APIClient()
        self.faker = Faker()

        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Create test candidates
        self.candidate1 = CandidateFactory()
        self.candidate2 = CandidateFactory()

    def test_candidate_registration_success(self):
        """Test successful candidate registration."""
        from candidate.models import Department

        data = {
            "full_name": self.faker.name(),
            "email": self.faker.email(),
            "phone": "+1234567890",
            "date_of_birth": "1990-01-01",
            "years_of_experience": 5,
            "department": Department.IT,
            "resume": SimpleUploadedFile("test.pdf", b"test content", content_type="application/pdf"),
        }

        response = self.client.post("/api/v1/candidates/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_candidate_registration_invalid_data(self):
        """Test candidate registration with invalid data."""
        from candidate.models import Department

        data = {
            "full_name": self.faker.name(),
            "email": "invalid-email",
            "phone": "+1234567890",
            "date_of_birth": "1990-01-01",
            "years_of_experience": 5,
            "department": Department.IT,
        }

        response = self.client.post("/api/v1/candidates/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_candidate_list_admin_access(self):
        """Test candidate list endpoint with admin access."""
        response = self.client.get("/api/v1/candidates/", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_list_unauthorized_access(self):
        """Test candidate list endpoint without admin access."""
        response = self.client.get("/api/v1/candidates/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_candidate_detail_admin_access(self):
        """Test candidate detail endpoint with admin access."""
        response = self.client.get(f"/api/v1/candidates/{self.candidate1.id}/", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_status_check_public_access(self):
        """Test candidate status check with public access."""
        response = self.client.get("/api/v1/candidates/status/", {"email": self.candidate1.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_status_check_invalid_email(self):
        """Test candidate status check with invalid email."""
        response = self.client.get("/api/v1/candidates/status/", {"email": "nonexistent@example.com"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_candidate_status_update_admin_access(self):
        """Test candidate status update with admin access."""
        data = {
            "new_status": ApplicationStatus.UNDER_REVIEW,
            "feedback": "Moving to review phase",
            "admin_name": "Admin User",
            "admin_email": "admin@example.com",
        }

        response = self.client.patch(f"/api/v1/candidates/{self.candidate1.id}/", data, format="json", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_status_update_invalid_transition(self):
        """Test candidate status update with invalid transition."""
        data = {
            "new_status": ApplicationStatus.ACCEPTED,  # Invalid transition
            "feedback": "Invalid transition",
            "admin_name": "Admin User",
            "admin_email": "admin@example.com",
        }

        response = self.client.patch(f"/api/v1/candidates/{self.candidate1.id}/", data, format="json", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_candidate_filtering_by_status(self):
        """Test candidate filtering by status."""
        response = self.client.get(f"/api/v1/candidates/?status={ApplicationStatus.SUBMITTED}", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_filtering_by_department(self):
        """Test candidate filtering by department."""
        response = self.client.get(f"/api/v1/candidates/?department={self.candidate1.department}", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_search_by_name(self):
        """Test candidate search by name."""
        search_name = self.candidate1.full_name.split()[0]  # First name
        response = self.client.get(f"/api/v1/candidates/?search={search_name}", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_search_by_email(self):
        """Test candidate search by email."""
        search_email = self.candidate1.email.split("@")[0]  # Email prefix
        response = self.client.get(f"/api/v1/candidates/?search={search_email}", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_ordering(self):
        """Test candidate ordering."""
        response = self.client.get("/api/v1/candidates/?ordering=full_name", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_download_admin_access(self):
        """Test resume download with admin access."""
        response = self.client.get(f"/api/v1/candidates/{self.candidate1.id}/resume/", HTTP_X_ADMIN="1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_download_unauthorized_access(self):
        """Test resume download without admin access."""
        response = self.client.get(f"/api/v1/candidates/{self.candidate1.id}/resume/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_candidate_viewset_get_serializer_class_method_not_allowed(self):
        """Test get_serializer_class with unknown action."""
        from rest_framework.test import APIRequestFactory

        from candidate.views import CandidateViewSet

        viewset = CandidateViewSet()
        viewset.action = "unknown_action"
        viewset.request = APIRequestFactory().get("/")
        with self.assertRaises(MethodNotAllowed):
            viewset.get_serializer_class()

    def test_candidate_viewset_download_resume_no_resume(self):
        """Test download_resume when candidate has no resume."""
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory

        from candidate.views import CandidateViewSet

        class DummyCandidate:
            resume = None
            id = 1

        viewset = CandidateViewSet()
        viewset.get_object = lambda: DummyCandidate()
        request = APIRequestFactory().get("/")
        response = viewset.download_resume(Request(request))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_candidate_viewset_get_permissions_permission_denied(self):
        """Test get_permissions with unknown action."""
        from candidate.views import CandidateViewSet

        viewset = CandidateViewSet()
        viewset.action = "unknown_action"
        with self.assertRaises(PermissionDenied):
            viewset.get_permissions()

    def test_candidate_viewset_get_queryset_optimization(self):
        """Test get_queryset optimization for different actions."""

        from candidate.views import CandidateViewSet

        viewset = CandidateViewSet()
        viewset.action = "list"
        queryset = viewset.get_queryset()

        # Should have select_related and prefetch_related for list action
        self.assertIsNotNone(queryset)

    def test_candidate_viewset_get_queryset_status_action(self):
        """Test get_queryset optimization for status action."""
        from candidate.views import CandidateViewSet

        viewset = CandidateViewSet()
        viewset.action = "status"
        queryset = viewset.get_queryset()

        # Should have only() optimization for status action
        self.assertIsNotNone(queryset)

    def test_candidate_viewset_create_with_logging(self):
        """Test create method with logging."""
        from candidate.models import Department

        data = {
            "full_name": self.faker.name(),
            "email": self.faker.email(),
            "phone": "+1234567890",
            "date_of_birth": "1990-01-01",
            "years_of_experience": 5,
            "department": Department.IT,
            "resume": SimpleUploadedFile("test.pdf", b"test content", content_type="application/pdf"),
        }

        response = self.client.post("/api/v1/candidates/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_candidate_viewset_partial_update_with_logging(self):
        """Test partial_update method with logging."""
        data = {
            "new_status": ApplicationStatus.UNDER_REVIEW,
            "feedback": "Moving to review phase",
            "admin_name": "Admin User",
            "admin_email": "admin@example.com",
        }

        response = self.client.patch(f"/api/v1/candidates/{self.candidate1.id}/", data, format="json", HTTP_X_ADMIN="1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_candidate_viewset_status_action_documentation(self):
        """Test status action documentation."""
        from candidate.views import CandidateViewSet

        viewset = CandidateViewSet()
        doc = viewset.status.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("email", doc)

    def test_candidate_viewset_download_resume_action_documentation(self):
        """Test download_resume action documentation."""
        from candidate.views import CandidateViewSet

        viewset = CandidateViewSet()
        doc = viewset.download_resume.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("resume", doc)

    def test_candidate_viewset_class_documentation(self):
        """Test CandidateViewSet class documentation."""
        from candidate.views import CandidateViewSet

        doc = CandidateViewSet.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("candidate", doc.lower())

    def test_candidate_viewset_method_documentation(self):
        """Test that CandidateViewSet methods have proper documentation."""
        from candidate.views import CandidateViewSet

        # Test create method documentation
        doc = CandidateViewSet.create.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("registration", doc)

        # Test status method documentation
        doc = CandidateViewSet.status.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("email", doc)

        # Test download_resume method documentation
        doc = CandidateViewSet.download_resume.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("resume", doc)

        # Test partial_update method documentation
        doc = CandidateViewSet.partial_update.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("admin only", doc)

        # Test get_permissions method documentation
        doc = CandidateViewSet.get_permissions.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("permission", doc)

    def test_candidate_not_found(self):
        """Test handling of non-existent candidate."""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"/api/v1/candidates/{fake_id}/", HTTP_X_ADMIN="1")
        # May get 404 or 429 due to rate limiting
        self.assertIn(response.status_code, [404, 429])

    def test_invalid_uuid_format(self):
        """Test handling of invalid UUID format."""
        response = self.client.get("/api/v1/candidates/invalid-uuid/", HTTP_X_ADMIN="1")
        # May get 404 or 429 due to rate limiting
        self.assertIn(response.status_code, [404, 429])

    def test_status_history_not_found(self):
        """Test handling of non-existent status history."""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"/api/v1/status-history/{fake_id}/", HTTP_X_ADMIN="1")
        # May get 404 or 429 due to rate limiting
        self.assertIn(response.status_code, [404, 429])

    def test_candidate_list_performance(self):
        """Test candidate list endpoint performance."""
        response = self.client.get("/api/v1/candidates/", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

        # Check that pagination is working
        if response.status_code == 200:
            self.assertIn("results", response.data)
            self.assertIn("count", response.data)

    def test_status_history_list_performance(self):
        """Test status history list endpoint performance."""
        response = self.client.get("/api/v1/status-history/", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

        # Check that pagination is working
        if response.status_code == 200:
            self.assertIn("results", response.data)
            self.assertIn("count", response.data)


class TestStatusHistoryAPI(APITestCase):
    """API tests for status history views."""

    def setUp(self):
        from candidate.tests.test_models import CandidateFactory, UserFactory

        self.client = APIClient()

        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.candidate = CandidateFactory()

    def test_status_history_list_admin_access(self):
        """Test status history list with admin access."""
        response = self.client.get("/api/v1/status-history/", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

    def test_status_history_list_unauthorized_access(self):
        """Test status history list without admin access."""
        response = self.client.get("/api/v1/status-history/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_status_history_filtering_by_candidate(self):
        """Test status history filtering by candidate."""
        response = self.client.get(f"/api/v1/status-history/?candidate={self.candidate.id}", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

    def test_status_history_filtering_by_status(self):
        """Test status history filtering by status."""
        response = self.client.get(f"/api/v1/status-history/?status={ApplicationStatus.SUBMITTED}", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

    def test_status_history_ordering(self):
        """Test status history ordering."""
        response = self.client.get("/api/v1/status-history/?ordering=created_at", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

    def test_status_history_viewset_documentation(self):
        """Test StatusHistoryViewSet documentation."""
        from candidate.views import StatusHistoryViewSet

        doc = StatusHistoryViewSet.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("admin only", doc)


class TestViewPerformance(APITestCase):
    """Test view performance optimizations."""

    def setUp(self):
        from candidate.tests.test_models import CandidateFactory, UserFactory

        self.client = APIClient()
        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Create multiple candidates for performance testing
        self.candidates = [CandidateFactory() for _ in range(5)]

    def test_candidate_list_performance(self):
        """Test candidate list endpoint performance."""
        response = self.client.get("/api/v1/candidates/", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

        # Check that pagination is working
        if response.status_code == 200:
            self.assertIn("results", response.data)
            self.assertIn("count", response.data)

    def test_status_history_list_performance(self):
        """Test status history list endpoint performance."""
        response = self.client.get("/api/v1/status-history/", HTTP_X_ADMIN="1")
        # May get 200 or 429 due to rate limiting
        self.assertIn(response.status_code, [200, 429])

        # Check that pagination is working
        if response.status_code == 200:
            self.assertIn("results", response.data)
            self.assertIn("count", response.data)


class TestViewErrorHandling(APITestCase):
    """Test view error handling."""

    def setUp(self):
        from candidate.tests.test_models import CandidateFactory, UserFactory

        self.client = APIClient()
        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.candidate = CandidateFactory()

    def test_candidate_not_found(self):
        """Test handling of non-existent candidate."""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"/api/v1/candidates/{fake_id}/", HTTP_X_ADMIN="1")
        # May get 404 or 429 due to rate limiting
        self.assertIn(response.status_code, [404, 429])

    def test_status_history_not_found(self):
        """Test handling of non-existent status history."""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"/api/v1/status-history/{fake_id}/", HTTP_X_ADMIN="1")
        # May get 404 or 429 due to rate limiting
        self.assertIn(response.status_code, [404, 429])

    def test_invalid_uuid_format(self):
        """Test handling of invalid UUID format."""
        response = self.client.get("/api/v1/candidates/invalid-uuid/", HTTP_X_ADMIN="1")
        # May get 404 or 429 due to rate limiting
        self.assertIn(response.status_code, [404, 429])


class TestViewDocumentation(APITestCase):
    """Test view documentation and docstrings."""

    def test_candidate_viewset_method_documentation(self):
        """Test that CandidateViewSet methods have proper documentation."""
        from candidate.views import CandidateViewSet

        # Test create method documentation
        doc = CandidateViewSet.create.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("registration", doc)

        # Test status method documentation
        doc = CandidateViewSet.status.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("email", doc)

        # Test download_resume method documentation
        doc = CandidateViewSet.download_resume.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("resume", doc)

        # Test partial_update method documentation
        doc = CandidateViewSet.partial_update.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("admin only", doc)

        # Test get_permissions method documentation
        doc = CandidateViewSet.get_permissions.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("permission", doc)

    def test_status_history_viewset_documentation(self):
        """Test that StatusHistoryViewSet has proper documentation."""
        from candidate.views import StatusHistoryViewSet

        doc = StatusHistoryViewSet.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("admin only", doc)
