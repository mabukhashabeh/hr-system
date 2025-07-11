from rest_framework.routers import DefaultRouter

from candidate.views import CandidateViewSet, StatusHistoryViewSet

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'status-history', StatusHistoryViewSet, basename='status-history')

app_name = 'candidate'

urlpatterns = router.urls

