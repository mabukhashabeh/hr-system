import logging

from django.utils import timezone

from core.tasks import send_email_task

logger = logging.getLogger(__name__)


def send_registration_email(candidate):
    """Send registration confirmation email asynchronously."""
    try:
        context = {
            "recipient_name": candidate.full_name,
            "recipient_email": candidate.email,
            "department": candidate.department,
            "registration_date": timezone.now().strftime("%B %d, %Y"),
            "application_id": str(candidate.id),
        }
        subject = "Application Received - HR System"

        send_email_task.delay(
            template_name="registration_confirmation",
            context=context,
            subject=subject,
            recipient_email=candidate.email,
            recipient_name=candidate.full_name,
        )
        logger.info(f"Registration email queued for {candidate.email}")

    except Exception as e:
        logger.error(f"Error queuing registration email for {candidate.email}: {str(e)}")


def send_status_update_email(candidate, new_status, previous_status, update_data):
    """Send status update email asynchronously."""
    try:
        context = {
            "recipient_name": candidate.full_name,
            "recipient_email": candidate.email,
            "previous_status": previous_status,
            "new_status": new_status,
            "feedback": update_data.get("feedback", ""),
            "admin_name": update_data.get("admin_name", "HR Team"),
            "update_date": timezone.now().strftime("%B %d, %Y at %I:%M %p"),
            "application_id": str(candidate.id),
        }
        subject = f"Application Status Updated - {new_status.replace('_', ' ').title()}"

        send_email_task.delay(
            template_name="status_update",
            context=context,
            subject=subject,
            recipient_email=candidate.email,
            recipient_name=candidate.full_name,
        )

        logger.info(f"Status update email queued for {candidate.email}: {previous_status} -> {new_status}")

    except Exception as e:
        logger.error(f"Error queuing status update email for {candidate.email}: {str(e)}")
