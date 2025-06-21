from django.contrib.auth.mixins import LoginRequiredMixin as _LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

class LoginRequiredMixin(_LoginRequiredMixin):
    login_url = 'login'

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для просмотра этой страницы.')
        return super().handle_no_permission()
