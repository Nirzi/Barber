from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

STATUS_CHOICES = [
    ('new', 'Новая'),
    ('approved', 'Подтверждена'),
    ('completed', 'Завершена'),
    ('canceled', 'Отменена'),
]