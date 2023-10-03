from django.test import TestCase, Client, override_settings
from django.core import mail
from django.shortcuts import reverse

from orders.models import Order
from customers.models import Customer
from .models import Robot
import json


class RobotsTest(TestCase):
    def setUp(self):
        self.client: Client = Client()

    def test_post(self):
        data = {
            "model": "R2",
            "version": "D2",
            "created": "2023-10-02 23:59:59"
        }
        json_data = json.dumps(data)

        response = self.client.post(
            reverse('post_json'), json_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {'message': 'Data received successfully'}
        )

    # @override_settings(EMAIL_BACKEND='django.core.mail.backend.locmem.EmailBackend')
    def test_email_on_availability(self):
        robot_data = {
            "serial": "R2-D2",
            "model": "R2",
            "version": "D2",
            "created": "2023-10-02 23:59:59"
        }

        customer_data = {
            "email": "customer@test.com"
        }

        order_data = {
            "robot_serial": "R2-D2",
        }


        robot = Robot.objects.create(**robot_data)
        customer = Customer.objects.create(**customer_data)
        order = Order.objects.create(customer=customer, **order_data)
        
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        message = (
            "Добрый день!\n"
            f"Недавно вы интересовались нашим роботом модели {robot_data['model']}, версии {rpbot_data['version']} .\n"
            "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
        )
        self.assertEqual(email.subject, "R4C: Робот в наличии")
        self.assertIn(message)
