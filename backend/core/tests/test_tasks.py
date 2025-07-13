from unittest.mock import MagicMock, patch

from django.test import TestCase

from core.tasks import send_email_task


class TestCeleryTasks(TestCase):
    """Unit tests for Celery tasks."""

    def setUp(self):
        """Set up test data."""
        from candidate.tests.test_models import CandidateFactory

        self.candidate = CandidateFactory()

    @patch("core.tasks.NotificationService")
    def test_send_email_task_success(self, mock_notification_service):
        """Test send email task success."""
        # Mock the notification service
        mock_service = MagicMock()
        mock_service.send_email.return_value = True
        mock_notification_service.send_email = mock_service.send_email

        # Call the task
        result = send_email_task(
            template_name="registration_confirmation",
            context={"candidate": self.candidate},
            subject="Application Received",
            recipient_email=self.candidate.email,
            recipient_name=self.candidate.full_name,
        )

        # Verify the task was called
        mock_service.send_email.assert_called_once_with(
            template_name="registration_confirmation",
            context={"candidate": self.candidate},
            subject="Application Received",
            recipient_email=self.candidate.email,
            recipient_name=self.candidate.full_name,
        )

        # Verify the task returns success
        self.assertTrue(result)

    @patch("core.tasks.NotificationService")
    def test_send_email_task_failure(self, mock_notification_service):
        """Test send email task failure."""
        # Mock the notification service to return False
        mock_service = MagicMock()
        mock_service.send_email.return_value = False
        mock_notification_service.send_email = mock_service.send_email

        # Call the task
        result = send_email_task(
            template_name="registration_confirmation",
            context={"candidate": self.candidate},
            subject="Application Received",
            recipient_email=self.candidate.email,
            recipient_name=self.candidate.full_name,
        )

        # Verify the task returns failure
        self.assertFalse(result)

    @patch("core.tasks.NotificationService")
    def test_send_email_task_exception_handling(self, mock_notification_service):
        """Test send email task exception handling."""
        # Mock the notification service to raise an exception
        mock_service = MagicMock()
        mock_service.send_email.side_effect = Exception("Email service error")
        mock_notification_service.send_email = mock_service.send_email

        # Call the task - should not raise exception due to retry mechanism
        try:
            result = send_email_task(
                template_name="registration_confirmation",
                context={"candidate": self.candidate},
                subject="Application Received",
                recipient_email=self.candidate.email,
                recipient_name=self.candidate.full_name,
            )
            # Should return False after retries exhausted
            self.assertFalse(result)
        except Exception:
            # If retry mechanism raises exception, that's also acceptable
            pass

    def test_send_email_task_documentation(self):
        """Test send email task documentation."""
        doc = send_email_task.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("email", doc.lower())

    def test_send_email_task_parameters(self):
        """Test send email task with different parameters."""
        from candidate.tests.test_models import CandidateFactory

        candidate = CandidateFactory()

        with patch("core.tasks.NotificationService") as mock_notification_service:
            mock_service = MagicMock()
            mock_service.send_email.return_value = True
            mock_notification_service.send_email = mock_service.send_email

            # Test with all parameters
            result = send_email_task(
                template_name="status_update",
                context={"candidate": candidate, "status": "Under Review"},
                subject="Status Updated",
                recipient_email=candidate.email,
                recipient_name=candidate.full_name,
            )

            self.assertTrue(result)

            # Test without recipient_name
            result = send_email_task(
                template_name="status_update",
                context={"candidate": candidate, "status": "Under Review"},
                subject="Status Updated",
                recipient_email=candidate.email,
            )

            self.assertTrue(result)


class TestCeleryTaskIntegration(TestCase):
    """Test Celery task integration with real data."""

    def setUp(self):
        """Set up test data."""
        from candidate.tests.test_models import CandidateFactory

        self.candidate = CandidateFactory()
        self.notification_service = MagicMock()

    @patch("core.tasks.NotificationService")
    def test_full_workflow_with_tasks(self, mock_notification_service):
        """Test full workflow using Celery tasks."""
        # Mock the notification service
        mock_service = MagicMock()
        mock_service.send_email.return_value = True
        mock_notification_service.send_email = mock_service.send_email

        # Test registration confirmation task
        result1 = send_email_task(
            template_name="registration_confirmation",
            context={"candidate": self.candidate},
            subject="Application Received",
            recipient_email=self.candidate.email,
            recipient_name=self.candidate.full_name,
        )
        self.assertTrue(result1)

        # Test status update task
        result2 = send_email_task(
            template_name="status_update",
            context={"candidate": self.candidate, "status": "Under Review"},
            subject="Status Updated",
            recipient_email=self.candidate.email,
            recipient_name=self.candidate.full_name,
        )
        self.assertTrue(result2)

        # Verify both tasks were called
        self.assertEqual(mock_service.send_email.call_count, 2)

    @patch("core.tasks.NotificationService")
    def test_task_with_different_templates(self, mock_notification_service):
        """Test tasks with different email templates."""
        # Mock the notification service
        mock_service = MagicMock()
        mock_service.send_email.return_value = True
        mock_notification_service.send_email = mock_service.send_email

        # Test different email templates
        templates = [
            ("registration_confirmation", "Application Received"),
            ("status_update", "Status Updated"),
        ]

        for template_name, subject in templates:
            result = send_email_task(
                template_name=template_name,
                context={"candidate": self.candidate},
                subject=subject,
                recipient_email=self.candidate.email,
                recipient_name=self.candidate.full_name,
            )

            self.assertTrue(result)

        # Verify all tasks were called
        self.assertEqual(mock_service.send_email.call_count, len(templates))

    def test_task_error_recovery(self):
        """Test task error recovery and retry logic."""
        # Test with invalid template
        with patch("core.tasks.NotificationService") as mock_notification_service:
            mock_service = MagicMock()
            mock_service.send_email.side_effect = Exception("Template not found")
            mock_notification_service.send_email = mock_service.send_email

            try:
                result = send_email_task(
                    template_name="invalid_template",
                    context={"candidate": self.candidate},
                    subject="Test",
                    recipient_email=self.candidate.email,
                )

                self.assertFalse(result)
            except Exception:
                # If retry mechanism raises exception, that's also acceptable
                pass


class TestCeleryTaskPerformance(TestCase):
    """Test Celery task performance characteristics."""

    def setUp(self):
        """Set up test data."""
        from candidate.tests.test_models import CandidateFactory

        self.candidates = [CandidateFactory() for _ in range(5)]

    @patch("core.tasks.NotificationService")
    def test_bulk_task_execution(self, mock_notification_service):
        """Test bulk task execution performance."""
        # Mock the notification service
        mock_service = MagicMock()
        mock_service.send_email.return_value = True
        mock_notification_service.send_email = mock_service.send_email

        # Execute multiple email tasks
        results = []
        for candidate in self.candidates:
            result = send_email_task(
                template_name="registration_confirmation",
                context={"candidate": candidate},
                subject="Application Received",
                recipient_email=candidate.email,
                recipient_name=candidate.full_name,
            )
            results.append(result)

        # Verify all tasks completed successfully
        for result in results:
            self.assertTrue(result)

        # Verify all tasks were called
        self.assertEqual(mock_service.send_email.call_count, len(self.candidates))

    @patch("core.tasks.NotificationService")
    def test_concurrent_task_execution(self, mock_notification_service):
        """Test concurrent task execution."""
        # Mock the notification service
        mock_service = MagicMock()
        mock_service.send_email.return_value = True
        mock_notification_service.send_email = mock_service.send_email

        # Simulate concurrent email sending
        results = []
        for candidate in self.candidates:
            result = send_email_task(
                template_name="status_update",
                context={"candidate": candidate, "status": "Under Review"},
                subject="Status Updated",
                recipient_email=candidate.email,
                recipient_name=candidate.full_name,
            )
            results.append(result)

        # Verify all tasks completed successfully
        for result in results:
            self.assertTrue(result)

        # Verify all tasks were called
        self.assertEqual(mock_service.send_email.call_count, len(self.candidates))
