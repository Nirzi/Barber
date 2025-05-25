from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from core.models import Order
from core.utils.telegram import send_telegram_message
import asyncio

@receiver(m2m_changed, sender=Order.services.through)
def notify_admin_on_order_services(sender, instance, action, **kwargs):
    if action == 'post_add':
        client = instance.client_name
        phone = instance.phone
        comment = instance.comment
        date = instance.appointment_date.strftime('%d.%m.%Y %H:%M')
        services = instance.services.all()
        services_text = "\n".join([f"— {s.name} ({s.price}₽)" for s in services])
        message = (
            f"*Новая заявка!*\n"
            f"*Клиент:* {client}\n"
            f"*Телефон:* {phone}\n"
            f"*Дата:* {date}\n"
            f"*Комментарий:* {comment or '—'}\n"
            f"*Услуги:*\n{services_text}\n"
            f"[Открыть в админке](https://your-site.ru/admin/core/order/{instance.id}/change/)"
        )
        asyncio.run(send_telegram_message(message))
