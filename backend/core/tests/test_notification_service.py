from unittest.mock import patch

from django.test import TestCase

from core.notification_service import NotificationService


class TestNotificationService(TestCase):
    """Unit tests for NotificationService."""

    def setUp(self):
        self.service = NotificationService()
        self.test_context = {
            "candidate_name": "John Doe",
            "status": "Under Review",
            "feedback": "Your application is being reviewed",
        }
        self.test_subject = "Application Status Update"
        self.test_recipient_email = "john.doe@example.com"
        self.test_recipient_name = "John Doe"

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_success(self, mock_render, mock_send_mail):
        """Test successful email sending."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Test</html>", "Test plain text"]

        # Mock email sending
        mock_send_mail.return_value = 1  # 1 email sent

        result = self.service.send_email(
            template_name="status_update",
            context=self.test_context,
            subject=self.test_subject,
            recipient_email=self.test_recipient_email,
            recipient_name=self.test_recipient_name,
        )

        self.assertTrue(result)
        mock_render.assert_any_call("emails/status_update.html", self.test_context)
        mock_render.assert_any_call("emails/status_update.txt", self.test_context)
        mock_send_mail.assert_called_once()

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_without_recipient_name(self, mock_render, mock_send_mail):
        """Test email sending without recipient name."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Test</html>", "Test plain text"]

        # Mock email sending
        mock_send_mail.return_value = 1  # 1 email sent

        result = self.service.send_email(
            template_name="status_update",
            context=self.test_context,
            subject=self.test_subject,
            recipient_email=self.test_recipient_email,
        )

        self.assertTrue(result)
        # Should not add recipient_name to context
        self.assertNotIn("recipient_name", self.test_context)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_recipient_name(self, mock_render, mock_send_mail):
        """Test email sending with recipient name."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Test</html>", "Test plain text"]

        # Mock email sending
        mock_send_mail.return_value = 1  # 1 email sent

        result = self.service.send_email(
            template_name="status_update",
            context=self.test_context,
            subject=self.test_subject,
            recipient_email=self.test_recipient_email,
            recipient_name=self.test_recipient_name,
        )

        self.assertTrue(result)
        # Should add recipient_name to context
        expected_context = self.test_context.copy()
        expected_context["recipient_name"] = self.test_recipient_name
        mock_render.assert_any_call("emails/status_update.html", expected_context)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_failure(self, mock_render, mock_send_mail):
        """Test email sending failure."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Test</html>", "Test plain text"]

        # Mock email sending failure
        mock_send_mail.return_value = 0  # 0 emails sent

        result = self.service.send_email(
            template_name="status_update",
            context=self.test_context,
            subject=self.test_subject,
            recipient_email=self.test_recipient_email,
        )

        self.assertFalse(result)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_exception(self, mock_render, mock_send_mail):
        """Test email sending with exception."""
        # Mock template rendering to raise exception
        mock_render.side_effect = Exception("Template rendering failed")

        result = self.service.send_email(
            template_name="status_update",
            context=self.test_context,
            subject=self.test_subject,
            recipient_email=self.test_recipient_email,
        )

        self.assertFalse(result)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_send_mail_exception(self, mock_render, mock_send_mail):
        """Test email sending when send_mail raises exception."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Test</html>", "Test plain text"]

        # Mock send_mail to raise exception
        mock_send_mail.side_effect = Exception("SMTP error")

        result = self.service.send_email(
            template_name="status_update",
            context=self.test_context,
            subject=self.test_subject,
            recipient_email=self.test_recipient_email,
        )

        self.assertFalse(result)

    def test_send_email_static_method(self):
        """Test that send_email is a static method."""
        # Should be able to call without instantiating the class
        with patch.object(NotificationService, "send_email") as mock_method:
            mock_method.return_value = True
            result = NotificationService.send_email(
                template_name="test", context={}, subject="Test", recipient_email="test@example.com"
            )
            self.assertTrue(result)

    def test_notification_service_documentation(self):
        """Test that NotificationService has proper documentation."""
        doc = NotificationService.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("notification", doc)

    def test_send_email_method_documentation(self):
        """Test that send_email method has proper documentation."""
        doc = NotificationService.send_email.__doc__
        self.assertIsNotNone(doc)
        self.assertIn("template", doc)


class TestNotificationServiceIntegration(TestCase):
    """Integration tests for NotificationService."""

    def setUp(self):
        self.service = NotificationService()

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_real_templates(self, mock_render, mock_send_mail):
        """Test email sending with realistic template names."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Registration</html>", "Registration text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="registration_confirmation",
            context={"candidate_name": "Jane Doe"},
            subject="Registration Confirmation",
            recipient_email="jane.doe@example.com",
            recipient_name="Jane Doe",
        )

        self.assertTrue(result)
        mock_render.assert_any_call(
            "emails/registration_confirmation.html", {"candidate_name": "Jane Doe", "recipient_name": "Jane Doe"}
        )
        mock_render.assert_any_call(
            "emails/registration_confirmation.txt", {"candidate_name": "Jane Doe", "recipient_name": "Jane Doe"}
        )

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_complex_context(self, mock_render, mock_send_mail):
        """Test email sending with complex context data."""
        complex_context = {
            "candidate_name": "Alice Smith",
            "status": "Interview Scheduled",
            "feedback": "Your application has been reviewed and we would like to schedule an interview.",
            "interview_date": "2024-01-15",
            "interview_time": "10:00 AM",
            "location": "Conference Room A",
            "admin_name": "HR Manager",
            "admin_email": "hr@company.com",
        }

        # Mock template rendering
        mock_render.side_effect = ["<html>Complex</html>", "Complex text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="status_update",
            context=complex_context,
            subject="Interview Scheduled",
            recipient_email="alice.smith@example.com",
            recipient_name="Alice Smith",
        )

        self.assertTrue(result)
        expected_context = complex_context.copy()
        expected_context["recipient_name"] = "Alice Smith"
        mock_render.assert_any_call("emails/status_update.html", expected_context)


class TestNotificationServiceErrorHandling(TestCase):
    """Test NotificationService error handling."""

    def setUp(self):
        self.service = NotificationService()

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_empty_context(self, mock_render, mock_send_mail):
        """Test email sending with empty context."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Empty</html>", "Empty text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="test",
            context={},
            subject="Test",
            recipient_email="test@example.com",
        )

        self.assertTrue(result)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_none_context(self, mock_render, mock_send_mail):
        """Test email sending with None context."""
        # Mock template rendering
        mock_render.side_effect = ["<html>None</html>", "None text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="test",
            context=None,
            subject="Test",
            recipient_email="test@example.com",
        )

        self.assertTrue(result)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_empty_recipient_name(self, mock_render, mock_send_mail):
        """Test email sending with empty recipient name."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Empty</html>", "Empty text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="test",
            context={"test": "value"},
            subject="Test",
            recipient_email="test@example.com",
            recipient_name="",
        )

        self.assertTrue(result)
        # Empty string is falsy, so recipient_name should not be added to context
        expected_context = {"test": "value"}
        mock_render.assert_any_call("emails/test.html", expected_context)

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_none_recipient_name(self, mock_render, mock_send_mail):
        """Test email sending with None recipient name."""
        # Mock template rendering
        mock_render.side_effect = ["<html>None</html>", "None text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="test",
            context={"test": "value"},
            subject="Test",
            recipient_email="test@example.com",
            recipient_name=None,
        )

        self.assertTrue(result)
        # Should not add recipient_name to context when None
        expected_context = {"test": "value"}
        mock_render.assert_any_call("emails/test.html", expected_context)


class TestNotificationServicePerformance(TestCase):
    """Test NotificationService performance characteristics."""

    def setUp(self):
        self.service = NotificationService()

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_performance_multiple_calls(self, mock_render, mock_send_mail):
        """Test email sending performance with multiple calls."""
        # Mock template rendering
        mock_render.side_effect = ["<html>Test</html>", "Test text"] * 10

        # Mock email sending
        mock_send_mail.return_value = 1

        # Test multiple email sends
        for i in range(10):
            result = self.service.send_email(
                template_name="test",
                context={"index": i},
                subject=f"Test {i}",
                recipient_email=f"test{i}@example.com",
            )
            self.assertTrue(result)

        # Should have been called 10 times
        self.assertEqual(mock_send_mail.call_count, 10)
        self.assertEqual(mock_render.call_count, 20)  # HTML and text templates

    @patch("core.notification_service.send_mail")
    @patch("core.notification_service.render_to_string")
    def test_send_email_with_large_context(self, mock_render, mock_send_mail):
        """Test email sending with large context data."""
        large_context = {
            "candidate_name": "John Doe",
            "status": "Under Review",
            "feedback": "A" * 1000,  # Large feedback text
            "history": [{"date": "2024-01-01", "status": "Submitted"} for _ in range(100)],
            "metadata": {"source": "web", "ip": "192.168.1.1", "user_agent": "Mozilla/5.0"},
        }

        # Mock template rendering
        mock_render.side_effect = ["<html>Large</html>", "Large text"]

        # Mock email sending
        mock_send_mail.return_value = 1

        result = self.service.send_email(
            template_name="status_update",
            context=large_context,
            subject="Status Update",
            recipient_email="john.doe@example.com",
        )

        self.assertTrue(result)
        mock_render.assert_any_call("emails/status_update.html", large_context)
