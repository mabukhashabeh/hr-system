import pytest
from django.test import TestCase
from rest_framework.test import APIClient


class TestPermission(TestCase):
    """Unit tests for permissions."""
    
    def setUp(self):
        from candidate.tests.test_models import UserFactory
        
        self.client = APIClient()
        self.admin_user = UserFactory()
        self.admin_user.is_staff = True
        self.admin_user.save()
    
    def test_candidate_permission_allow_get(self):
        """Test candidate permission allows GET for status action."""
        from candidate.permissions import CandidatePermission
        
        class DummyView:
            action = 'status'
        
        class DummyRequest:
            method = 'GET'
        
        perm = CandidatePermission()
        self.assertTrue(perm.has_permission(DummyRequest(), DummyView()))
    
    def test_candidate_permission_allow_post(self):
        """Test candidate permission allows POST for create action."""
        from candidate.permissions import CandidatePermission
        
        class DummyView:
            action = 'create'
        
        class DummyRequest:
            method = 'POST'
        
        perm = CandidatePermission()
        self.assertTrue(perm.has_permission(DummyRequest(), DummyView()))
    
    def test_admin_permission_deny_anonymous(self):
        """Test admin permission denies anonymous users."""
        from candidate.permissions import AdminOnlyPermission
        
        class DummyView:
            action = 'list'
        
        class DummyRequest:
            headers = {}
        
        perm = AdminOnlyPermission()
        self.assertFalse(perm.has_permission(DummyRequest(), DummyView()))
    
    def test_admin_permission_allow_staff(self):
        """Test admin permission allows staff users."""
        from candidate.permissions import AdminOnlyPermission
        
        class DummyView:
            action = 'list'
        
        class DummyRequest:
            headers = {'X-ADMIN': '1'}
        
        perm = AdminOnlyPermission()
        self.assertTrue(perm.has_permission(DummyRequest(), DummyView()))
    
    def test_admin_only_permission_non_admin_action(self):
        """Test admin permission for non-admin actions."""
        from candidate.permissions import AdminOnlyPermission
        
        class DummyView:
            action = 'not_admin_action'
        
        class DummyRequest:
            headers = {}
        
        perm = AdminOnlyPermission()
        self.assertFalse(perm.has_permission(DummyRequest(), DummyView())) 