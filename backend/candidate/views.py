import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from candidate.filters import CandidateFilter, StatusHistoryFilter
from candidate.models import Candidate, StatusHistory
from candidate.permissions import AdminOnlyPermission, CandidatePermission
from candidate.serializers import (
    CandidateDetailSerializer,
    CandidateListSerializer,
    CandidateRegistrationSerializer,
    CandidateStatusSerializer,
    ResumeDownloadSerializer,
    StatusHistorySerializer,
    StatusUpdateSerializer,
)
from candidate.utils import send_registration_email, send_status_update_email

logger = logging.getLogger(__name__)


class CandidateViewSet(viewsets.ModelViewSet):
    """
    Candidate registration, listing, detail, status check, status update, resume download, and stats.
    Only required endpoints are implemented.
    """

    queryset = Candidate.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CandidateFilter
    ordering_fields = ["created_at", "full_name", "years_of_experience"]
    ordering = ["-created_at"]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        Raise MethodNotAllowed if action is not permitted.
        """
        serializer_classes = {
            "create": CandidateRegistrationSerializer,
            "list": CandidateListSerializer,
            "retrieve": CandidateDetailSerializer,
            "partial_update": StatusUpdateSerializer,
            "status": CandidateStatusSerializer,
            "download_resume": ResumeDownloadSerializer,
        }
        if not (serializer_class := serializer_classes.get(self.action)):
            raise MethodNotAllowed(self.request.method)
        return serializer_class

    def create(self, request, *args, **kwargs):
        """Handle candidate registration."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate = serializer.save()

        logger.info(f"New candidate registered: {candidate.full_name} ({candidate.email})")
        # Trigger registration confirmation email
        send_registration_email(candidate)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="status", url_name="status")
    def status(self, request, *args, **kwargs):
        """Check candidate status by email."""
        serializer = self.get_serializer(data=request.query_params, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="resume", url_name="download-resume")
    def download_resume(self, request, *args, **kwargs):
        """Get resume download URL for candidate."""
        candidate = self.get_object()
        if not candidate.resume:
            logger.warning(f"Resume download attempted for candidate {candidate.id} without resume")
            return Response({"error": "Resume not found for this candidate"}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"Resume download requested for candidate {candidate.full_name} ({candidate.email})")
        serializer = self.get_serializer(instance=candidate, context={"request": request})
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Update candidate status (admin only)."""
        candidate = self.get_object()
        serializer = self.get_serializer(
            instance=candidate, data=request.data, context={"request": request, "candidate": candidate}
        )
        serializer.is_valid(raise_exception=True)

        # Get the new status before updating for logging
        new_status = serializer.validated_data["new_status"]
        previous_status = candidate.current_status

        updated_candidate = serializer.update(candidate, serializer.validated_data)

        logger.info(f"Status updated for candidate {candidate.full_name}: {previous_status} -> {new_status}")

        # Trigger status update email
        send_status_update_email(
            candidate=updated_candidate,
            new_status=new_status,
            previous_status=previous_status,
            update_data=serializer.validated_data,
        )

        response_serializer = CandidateDetailSerializer(updated_candidate, context={"request": request})

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Return appropriate permissions based on the action."""
        if self.action in ["create", "status"]:
            return [CandidatePermission()]
        elif self.action in ["list", "retrieve", "partial_update", "download_resume"]:
            return [AdminOnlyPermission()]
        else:
            raise PermissionDenied()


class StatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for status history (admin only, with filtering).
    """

    queryset = StatusHistory.objects.select_related("candidate")
    serializer_class = StatusHistorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = StatusHistoryFilter
    ordering_fields = ["created_at", "candidate__full_name", "new_status"]
    ordering = ["-created_at"]
    permission_classes = [AdminOnlyPermission]
