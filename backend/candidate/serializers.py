from typing import Any

from rest_framework import serializers

from candidate.models import ApplicationStatus, Candidate, StatusHistory


class CandidateRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for candidate registration with comprehensive validation."""

    class Meta:
        model = Candidate
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "date_of_birth",
            "years_of_experience",
            "department",
            "resume",
            "age",
            "current_status",
            "created_at",
        ]
        read_only_fields = ["id", "current_status", "created_at", "age"]

    def get_age(self, obj) -> int:
        """Calculate and return candidate age."""
        return obj.age

    def create(self, validated_data: dict[str, Any]) -> Candidate:
        """Create candidate with initial status history."""
        candidate = super().create(validated_data)

        # Create initial status history
        StatusHistory.objects.create(
            candidate=candidate,
            new_status=ApplicationStatus.SUBMITTED,
            feedback="Application submitted successfully",
            admin_name="System",
            admin_email="admin@hr-system.me",
        )

        return candidate


class CandidateListSerializer(serializers.ModelSerializer):
    """Serializer for candidate listing (admin view)."""

    department = serializers.CharField(source="get_department_display", read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "years_of_experience",
            "department",
            "current_status",
            "created_at",
        ]

    def get_age(self, obj) -> int:
        """Calculate and return candidate age."""
        return obj.age


class StatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for status history."""

    previous_status = serializers.CharField(source="get_previous_status_display", read_only=True)
    new_status = serializers.CharField(source="get_new_status_display", read_only=True)
    admin_name = serializers.CharField(required=True)
    admin_email = serializers.EmailField(required=True)
    feedback = serializers.CharField(required=True)

    class Meta:
        model = StatusHistory
        fields = ["id", "previous_status", "new_status", "feedback", "admin_name", "admin_email", "created_at"]
        read_only_fields = ["id", "created_at"]


class CandidateStatusSerializer(serializers.ModelSerializer):
    """Serializer for candidate status tracking."""

    email = serializers.EmailField(required=True)
    current_status_display = serializers.CharField(source="get_current_status_display", read_only=True)
    department = serializers.CharField(source="get_department_display", read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)

    def validate_email(self, value):
        try:
            self.instance = Candidate.objects.get(email=value)
        except Candidate.DoesNotExist:
            raise serializers.ValidationError("Candidate with this email does not exist.")
        return value

    class Meta:
        model = Candidate
        fields = [
            "id",
            "email",
            "department",
            "full_name",
            "current_status",
            "current_status_display",
            "years_of_experience",
            "phone",
            "status_history",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "years_of_experience",
            "phone",
            "current_status",
            "created_at",
            "updated_at",
        ]


class StatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating candidate status (admin only)."""

    new_status = serializers.ChoiceField(choices=ApplicationStatus.choices, required=True)
    feedback = serializers.CharField(required=True, max_length=1000, help_text="Feedback for the status change")
    admin_name = serializers.CharField(max_length=255, required=True, help_text="Name of the admin making the change")
    admin_email = serializers.EmailField(required=True, help_text="Email of the admin making the change")

    VALID_STATUS_TRANSITIONS = {
        ApplicationStatus.SUBMITTED: [ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REJECTED],
        ApplicationStatus.UNDER_REVIEW: [ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.REJECTED],
        ApplicationStatus.INTERVIEW_SCHEDULED: [
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.UNDER_REVIEW,  # Allow going back for re-evaluation
        ],
        ApplicationStatus.REJECTED: [],  # Final state
        ApplicationStatus.ACCEPTED: [],  # Final state
    }

    def validate_new_status(self, value):
        """Validate status transition logic."""
        candidate = self.context.get("candidate")
        if not candidate:
            return value

        current_status = candidate.current_status

        if value not in self.VALID_STATUS_TRANSITIONS.get(current_status, []):
            valid_transitions = self.VALID_STATUS_TRANSITIONS.get(current_status, [])
            raise serializers.ValidationError(
                f"Cannot transition from {current_status} to {value}. "
                f"Valid transitions: {', '.join(valid_transitions) if valid_transitions else 'No valid transitions'}"
            )

        return value

    def update(self, instance, validated_data):
        """Update candidate status and create history record."""
        previous_status = instance.current_status
        new_status = validated_data["new_status"]

        # Update candidate status
        instance.current_status = new_status
        instance.save(update_fields=["current_status", "updated_at"])

        # Create status history
        StatusHistory.objects.create(
            candidate=instance,
            previous_status=previous_status,
            new_status=new_status,
            feedback=validated_data["feedback"],
            admin_name=validated_data["admin_name"],
            admin_email=validated_data["admin_email"],
        )

        return instance


class CandidateDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for candidate information."""

    age = serializers.SerializerMethodField()
    department = serializers.CharField(source="get_department_display", read_only=True)
    current_status = serializers.CharField(source="get_current_status_display", read_only=True)
    status_history = StatusHistorySerializer(many=True, read_only=True)
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "date_of_birth",
            "age",
            "years_of_experience",
            "department",
            "current_status",
            "resume_url",
            "status_history",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_age(self, obj) -> int:
        """Calculate and return candidate age."""
        return obj.age

    def get_resume_url(self, obj) -> str:
        """Get resume download URL."""
        if (request := self.context.get("request")) and obj.resume:
            return request.build_absolute_uri(obj.resume.url)
        return ""


class ResumeDownloadSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ["id", "download_url"]

    def get_download_url(self, obj):
        if obj.resume:
            return obj.resume.url
