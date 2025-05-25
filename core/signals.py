from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from core.models import Order, Review
from core.utils.telegram import send_telegram_message
import asyncio


@receiver(post_save, sender=Order)
def notify_admin_on_order_save(sender, instance, created, **kwargs):
    if created:
        message = (
            f"*Новая заявка!*\n"
            f"*Клиент:* {instance.client_name}\n"
            f"*Телефон:* {instance.phone}\n"
            f"*Дата:* {instance.appointment_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"*Комментарий:* {instance.comment or '—'}\n"
            f"[Открыть в админке](http://127.0.0.1:8000/admin/core/order/{instance.id}/change/)"
        )
        asyncio.run(send_telegram_message(
            settings.TELEGRAM_BOT_TOKEN,
            settings.TELEGRAM_ADMIN_CHAT_ID,
            message
        ))


@receiver(post_save, sender=Review)
def notify_admin_on_review_save(sender, instance, created, **kwargs):
    if created and instance.is_published:
        message = (
            f"*Новый отзыв!*\n"
            f"*Клиент:* {instance.client_name}\n"
            f"*Оценка:* {instance.rating}⭐\n"
            f"*Мастер:* {instance.master.name}\n"
            f"*Текст:* {instance.text[:100]}...\n"
            f"[Открыть в админке](http://127.0.0.1:8000/admin/core/review/{instance.id}/change/)"
        )
        asyncio.run(send_telegram_message(
            settings.TELEGRAM_BOT_TOKEN,
            settings.TELEGRAM_ADMIN_CHAT_ID,
            message
        ))
