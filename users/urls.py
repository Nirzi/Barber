from django.urls import path
# Импортируем все наши представления
from .views import (
    UserRegisterView, UserLoginView, UserLogoutView,
    UserProfileDetailView, UserProfileUpdateView,
    UserPasswordChangeView, UserPasswordChangeDoneView, # Для success_url PasswordChangeView
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Профиль пользователя
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),

    # Смена пароля (внутри системы, для залогиненных пользователей)
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),

    # Восстановление пароля (для забывших)
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # uidb64 и token обязательны для PasswordResetConfirmView
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]