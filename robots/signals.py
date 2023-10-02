from django.db.models.signals import Signal, post_save
from django.dispatch import reciever
from django.core.mail import send_mail
from orders.models import Order
from .models import Robot


robot_created = Signal()
order_saved = Signal()


@reciever(post_save, sender=Robot)
def check_robot_availability(sender, instance, created, **kwargs):
    if created:
        try:
            orders = Order.objects.filter(robot_serial=instance.serial)
            if orders.exist():
                order_saved.send(sender=Order, orders=orders)
            except Order.DoesNotExist:
                pass


@reciever(order_saved, sender=Order)
def send_robot_available_email(sender, orders, **kwargs):
    for order in orders:
        try:
            subject = "R4C: Робот в наличии" 
            message = (
                "Добрый день!\n"
                f"Недавно вы интересовались нашим роботом модели {model}, версии {version} .\n"
                "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
            )
            from_email = "info@r4c.com" 
            to_emails = [order.customer.email]

            send_mail(subject, message, from_email, to_emails)
