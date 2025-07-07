from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages

# Убедитесь, что пути импорта верны для вашего проекта
# Используем новую форму
from .forms import SinglePasswordUserRegisterForm, UserLoginForm


# Пример функции для 'landing' страницы, если у вас ее нет
def landing_page(request):
    return render(
        request, "landing.html"
    )  # Убедитесь, что у вас есть templates/landing.html


class UserRegisterView(CreateView):
    # Используем SinglePasswordUserRegisterForm
    form_class = SinglePasswordUserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("landing")  # Или на другую страницу, например, 'profile'

    def form_valid(self, form):
        user = form.save()  # form.save() теперь сам хеширует пароль
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрированы и вошли в систему.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("--- ОШИБКИ ФОРМЫ РЕГИСТРАЦИИ (Single Password) ---")
        print("Объект формы:", form)
        print("Состояние валидности:", form.is_valid())
        print("Ошибки полей:", form.errors)

        if form.non_field_errors():
            print("Общие ошибки формы:", form.non_field_errors())

        for field_name, errors in form.errors.items():
            print(f"Ошибки для поля '{field_name}':")
            for error in errors:
                print(f"  - {error}")
        print("--- КОНЕЦ ОШИБОК ---")

        messages.error(
            self.request, "Пожалуйста, исправьте ошибки в форме регистрации."
        )
        return super().form_invalid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(
            self.request, f"Добро пожаловать, {self.request.user.username}!"
        )
        return reverse_lazy("landing")

    def form_invalid(self, form):
        print("--- ОШИБКИ ФОРМЫ ВХОДА ---")
        print("Ошибки полей:", form.errors)
        if form.non_field_errors():
            print("Общие ошибки формы:", form.non_field_errors())
        print("--- КОНЕЦ ОШИБОК ВХОДА ---")
        messages.error(
            self.request,
            "Неверное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.",
        )
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы вышли из системы.")
        return super().dispatch(request, *args, **kwargs)
