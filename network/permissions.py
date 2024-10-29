from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    """
    Проверка права доступа для пользователей с ролью "сотрудник".

    Этот класс проверяет, является ли пользователь сотрудником системы. Если да, то доступ разрешен, иначе - запрещен.
    """

    def has_permission(self, request, view):
        """
        Проверяет наличие прав доступа у текущего пользователя.

        :param request: HTTP-запрос.
        :param view: Представление, к которому осуществляется запрос.
        :return: True, если пользователь аутентифицирован и имеет статус сотрудника, иначе False.
        """

        return request.user and request.user.is_staff
