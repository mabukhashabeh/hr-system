import logging
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class NotificationService:
    """Simple notification service for sending emails."""

    @staticmethod
    def send_email(
        template_name: str, context: dict[str, Any], subject: str, recipient_email: str, recipient_name: str = None
    ) -> bool:
        """
        Send email using template and context.

        Args:
            template_name: Template name without extension
            context: Template context data
            subject: Email subject
            recipient_email: Recipient email address
            recipient_name: Recipient name (optional)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Add recipient name to context if provided
            if recipient_name:
                context["recipient_name"] = recipient_name

            # Render templates
            html_message = render_to_string(f"emails/{template_name}.html", context)
            plain_message = render_to_string(f"emails/{template_name}.txt", context)

            # Send email
            success = send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )

            if success:
                logger.info(f"Email sent successfully to {recipient_email}: {subject}")
                return True
            else:
                logger.error(f"Failed to send email to {recipient_email}: {subject}")
                return False

        except Exception as e:
            logger.error(f"Error sending email to {recipient_email}: {str(e)}")
            return False
