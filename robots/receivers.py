from django.db.models.signals import Signal, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from orders.models import Order
from .models import Robot


@receiver(post_save, sender=Robot)
def send_email_on_availabilty(sender, instance, created, **kwargs):
    if created:
        try:
            orders = Order.objects.filter(robot_serial=instance.serial)
            data = Robot.objects.get(serial=instance.serial)
            if orders.exists():
                subject = "R4C: Робот в наличии" 
                message = (
                    "Добрый день!\n"
                    f"Недавно вы интересовались нашим роботом модели {data.model}, версии {data.version} .\n"
                    "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
                )
                from_email = "info@r4c.com" 
                to_emails = list(orders.values_list('customer__email', flat=True))

                send_mail(subject, message, from_email, to_emails)
        except Order.DoesNotExist:
            pass

