from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIRequestFactory

from network.permissions import IsStaff


class MockView(APIView):
    permission_classes = [IsStaff]


class IsStaffPermissionTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MockView.as_view()

    def test_has_permission_when_user_is_not_staff(self):
        user = self._get_mock_user(is_staff=False)
        request = self.factory.get('/api/nodes/')
        request.user = user
        response = self.view(request)
        self.assertTrue(response.status_code == 403)

    def _get_mock_user(self, is_staff):
        class MockUser:
            def __init__(self, is_staff):
                self.is_staff = is_staff
                self.is_active = True
        return MockUser(is_staff)
