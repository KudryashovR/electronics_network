from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIRequestFactory

from network.permissions import IsStaff


class MockView(APIView):
    """
    Mock View для тестирования разрешений.

    Этот класс используется для имитации представления, защищенного разрешением IsStaff.
    """

    permission_classes = [IsStaff]


class IsStaffPermissionTests(APITestCase):
    """
    Тестовый кейс для проверки разрешения IsStaff.

    Этот класс включает методы для тестирования поведения разрешения IsStaff.
    """

    def setUp(self):
        """
        Установка тестовой среды.

        Создается фабрика запросов и представление для тестирования.
        """

        self.factory = APIRequestFactory()
        self.view = MockView.as_view()

    def test_has_permission_when_user_is_not_staff(self):
        """
        Тестирование разрешения при отсутствии статуса staff у пользователя.

        Проверяет, что пользователь без статуса staff получает отказ в доступе (код состояния 403).
        """

        user = self._get_mock_user(is_staff=False)
        request = self.factory.get('/api/nodes/')
        request.user = user
        response = self.view(request)
        self.assertTrue(response.status_code == 403)

    def _get_mock_user(self, is_staff):
        """
        Создание мока пользователя.

        Создает объект пользователя с заданными параметрами.

        :param is_staff: Флаг, определяющий статус staff пользователя.
        :return: Объект пользователя.
        """

        class MockUser:
            """
            Мок пользователя.

            Используется для симуляции пользователя в тестах.
            """

            def __init__(self, is_staff):
                """
                Конструктор мока пользователя.

                Устанавливает параметры пользователя.

                :param is_staff: Флаг, определяющий статус staff пользователя.
                """

                self.is_staff = is_staff
                self.is_active = True

        return MockUser(is_staff)
