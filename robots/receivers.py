from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from R4C import settings

from orders.models import Order
from .models import Robot


@receiver(post_save, sender=Robot)
def send_email_on_availabilty(sender, instance, created, **kwargs):
    if created:
        try:
            orders = Order.objects.filter(robot_serial=instance.serial)
            if orders.exists():
                subject = "R4C: Робот в наличии"

                message = f"""Добрый день!
Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."""  # noqa

                from_email = settings.EMAIL_HOST_USER
                to_emails = orders.values_list('customer__email', flat=True)

                send_mail(subject, message, from_email, to_emails)
        except Order.DoesNotExist:
            pass
