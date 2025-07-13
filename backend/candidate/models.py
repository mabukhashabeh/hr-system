import uuid
from datetime import datetime
from pathlib import Path

from django.db import models
from django.utils import timezone

from core.validators import (
    age_validator,
    experience_validator,
    file_size_validator,
    file_type_validator,
    phone_number_validator,
)


def candidate_resume_path(instance, filename):
    """Generate a unique, safe and structured path for candidate resumes."""
    ext = Path(filename).suffix
    name = "".join(c for c in Path(filename).stem.lower().replace(" ", "_") if c.isalnum() or c in "_-")[:40]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    return f"resumes/{instance.department}/{instance.id}/{name}_{timestamp}{ext}"


class Department(models.TextChoices):
    IT = "it", "Information Technology"
    HR = "hr", "Human Resources"
    FINANCE = "finance", "Finance"


class ApplicationStatus(models.TextChoices):
    SUBMITTED = "submitted", "Submitted"
    UNDER_REVIEW = "under_review", "Under Review"
    INTERVIEW_SCHEDULED = "interview_scheduled", "Interview Scheduled"
    REJECTED = "rejected", "Rejected"
    ACCEPTED = "accepted", "Accepted"


class Candidate(models.Model):
    """Candidate model with optimized database structure."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, validators=[phone_number_validator])
    date_of_birth = models.DateField(validators=[age_validator])
    years_of_experience = models.PositiveIntegerField(
        validators=[experience_validator],
    )
    department = models.CharField(max_length=10, choices=Department.choices, db_index=True)
    resume = models.FileField(
        upload_to=candidate_resume_path,
        max_length=500,
        validators=[file_size_validator, file_type_validator],
    )
    current_status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.SUBMITTED, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "candidates"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["department", "created_at"]),
            models.Index(fields=["current_status", "created_at"]),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.department}"

    @property
    def age(self):
        """Calculate age from date of birth."""
        if not self.date_of_birth:
            return None
        today = timezone.now().date()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )


class StatusHistory(models.Model):
    """Track all status changes with admin information."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="status_history")
    previous_status = models.CharField(max_length=20, choices=ApplicationStatus.choices, blank=True, null=True)
    new_status = models.CharField(max_length=20, choices=ApplicationStatus.choices)
    feedback = models.TextField(blank=True)
    admin_name = models.CharField(max_length=255, default="System Admin")
    admin_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "status_history"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["candidate", "created_at"]),
        ]

    def __str__(self):
        return f"{self.candidate.full_name}: {self.previous_status} -> {self.new_status}"
