from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin # AccessMixin для перенаправления аутентифицированных пользователей

# Импортируем наши формы
from .forms import (
    UserRegisterForm, UserLoginForm,
    UserProfileUpdateForm, UserPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)
# Импортируем модель User и UserProfile
from django.contrib.auth.models import User
from .models import UserProfile


# Пример функции для 'landing' страницы
def landing_page(request):
    return render(
        request, "landing.html"
    )

# Пользовательский миксин для перенаправления аутентифицированных пользователей
class RedirectAuthenticatedUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

# 3. UserRegisterView
class UserRegisterView(RedirectAuthenticatedUserMixin, CreateView): # Добавляем миксин
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("landing") # Или 'profile_detail' для только что зарегистрированного пользователя

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрированы и вошли в систему.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("--- ОШИБКИ ФОРМЫ РЕГИСТРАЦИИ ---")
        print("Ошибки полей:", form.errors)
        if form.non_field_errors():
            print("Общие ошибки формы:", form.non_field_errors())
        for field_name, errors in form.errors.items():
            print(f"  Ошибки для поля '{field_name}': {', '.join(errors)}")
        print("--- КОНЕЦ ОШИБОК ---")
        messages.error(
            self.request, "Пожалуйста, исправьте ошибки в форме регистрации."
        )
        return super().form_invalid(form)

# 4. UserLoginView
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True # Перенаправляет уже вошедших пользователей

    def get_success_url(self):
        # Обработка параметра next для перенаправления после входа
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse_lazy("landing") # По умолчанию на landing

    def form_valid(self, form):
        messages.success(
            self.request, f"Добро пожаловать, {form.get_user().username}!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Неверное имя пользователя или пароль. Пожалуйста, попробуйте еще раз."
        )
        return super().form_invalid(form)

# 5. UserLogoutView
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login") # Или на 'landing'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы вышли из системы.")
        return super().dispatch(request, *args, **kwargs)

# 6. UserProfileDetailView
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile # Используем модель UserProfile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile' # Имя объекта в шаблоне

    # Проверка принадлежности профиля
    def get_object(self, queryset=None):
        # Получаем пользователя из URL (pk)
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_pk) # Получаем объект User по PK

        # Если текущий пользователь не является владельцем профиля, и не является админом, перенаправляем
        if self.request.user != user and not self.request.user.is_staff:
            messages.error(self.request, "У вас нет прав для просмотра этого профиля.")
            return redirect(reverse_lazy('landing')) # Или на свой профиль
            # raise Http404("Нет доступа к этому профилю.") # Можно также выдать 404

        # Возвращаем связанный профиль пользователя
        return user.userprofile # Возвращаем объект UserProfile

    # Добавляем объект User в контекст для удобства
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_object'] = self.object.user # Объект User связанный с UserProfile
        return context


# 7. UserProfileUpdateView
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm # Используем нашу новую форму
    template_name = 'users/profile_update_form.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Редактировать можно только свой профиль
        return self.request.user.userprofile

    def get_success_url(self):
        messages.success(self.request, "Профиль успешно обновлен.")
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.pk}) # Перенаправляем на свой профиль

    def get_form_kwargs(self):
        # Передаем объект User в форму для валидации username и email
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# 8. UserPasswordChangeView
class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm # Используем нашу новую форму
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('password_change_done') # Перенаправляем на страницу подтверждения смены пароля

    def form_valid(self, form):
        messages.success(self.request, "Ваш пароль успешно изменен.")
        return super().form_valid(form)

# Класс для страницы успешной смены пароля (Django по умолчанию использует 'password_change_done', но нам нужен шаблон)
class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeView): # Это просто заглушка для success_url
    template_name = 'users/password_change_done.html' # Создадим этот шаблон

# 9. CustomPasswordResetView
class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html' # Шаблон письма
    form_class = CustomPasswordResetForm # Наша форма
    success_url = reverse_lazy('password_reset_done') # Перенаправление после отправки

    def form_valid(self, form):
        messages.info(self.request, "Если ваш email зарегистрирован, вы получите инструкцию по сбросу пароля на почту.")
        return super().form_valid(form)

# 10. CustomPasswordResetDoneView
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

# 11. CustomPasswordResetConfirmView
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm # Наша форма
    success_url = reverse_lazy('password_reset_complete')

# 12. CustomPasswordResetCompleteView
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'