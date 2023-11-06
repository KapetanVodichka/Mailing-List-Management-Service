from django.contrib.auth.mixins import UserPassesTestMixin


class ManagerMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_manager


class UserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return not self.request.user.is_manager
