from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserProfile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Обязательное поле.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'password': 'Пароль',
            'password2': 'Повторите пароль',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].help_text = None
        if 'password' in self.fields:
            self.fields['password'].help_text = None
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

class UserProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ('avatar', 'birth_date', 'telegram_id', 'github_id')
        labels = {
            'avatar': 'Аватар',
            'birth_date': 'Дата рождения',
            'telegram_id': 'Telegram ID',
            'github_id': 'GitHub ID',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telegram_id': forms.TextInput(attrs={'class': 'form-control'}),
            'github_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise ValidationError("Это имя пользователя уже занято.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile.save()
        return profile


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите старый пароль'})
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'})
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'old_password' in self.fields:
            self.fields['old_password'].help_text = None
        if 'new_password1' in self.fields:
            self.fields['new_password1'].help_text = None
        if 'new_password2' in self.fields:
            self.fields['new_password2'].help_text = None


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'})
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем help_text для полей
        if 'new_password1' in self.fields:
            self.fields['new_password1'].help_text = None
        if 'new_password2' in self.fields:
            self.fields['new_password2'].help_text = None