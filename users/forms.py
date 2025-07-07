from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Импортируем PasswordHasher, чтобы хешировать пароль вручную
from django.contrib.auth.hashers import make_password

class SinglePasswordUserRegisterForm(forms.ModelForm):
    # Поле email
    email = forms.EmailField(
        required=True,
        help_text='Обязательное поле.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    # Поле пароля (только одно)
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password') # Больше нет 'password2'
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'password': 'Пароль',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # password уже определено выше с widget
        }

    # Валидация email, как и раньше
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    # Переопределяем метод save, чтобы вручную хешировать пароль
    def save(self, commit=True):
        user = super().save(commit=False) # Создаем объект пользователя, но не сохраняем его сразу
        password = self.cleaned_data["password"]
        user.set_password(password) # Хешируем пароль
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )