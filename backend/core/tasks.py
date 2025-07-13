import logging

from celery import shared_task

from .notification_service import NotificationService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(
    self, template_name: str, context: dict, subject: str, recipient_email: str, recipient_name: str = None
) -> bool:
    """
    Celery task to send email asynchronously.

    Args:
        template_name: Email template name
        context: Template context data
        subject: Email subject
        recipient_email: Recipient email
        recipient_name: Recipient name (optional)

    Returns:
        bool: True if email sent successfully
    """
    try:
        success = NotificationService.send_email(
            template_name=template_name,
            context=context,
            subject=subject,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
        )

        if success:
            logger.info(f"Email task completed successfully for {recipient_email}")
            return True
        else:
            logger.error(f"Email task failed for {recipient_email}")
            return False

    except Exception as exc:
        logger.error(f"Email task error for {recipient_email}: {str(exc)}")
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        return False
