from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    telegram_id = models.CharField(max_length=50, blank=True, verbose_name="Telegram ID")
    github_id = models.CharField(max_length=50, blank=True, verbose_name="GitHub ID")

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

# Сигналы для автоматического создания и обновления UserProfile при создании/обновлении User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()