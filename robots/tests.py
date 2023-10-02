from django.test import TestCase, Client
from django.shortcuts import reverse
import json


class RobotModelsTest(TestCase):
    def setUp(self):
        self.client: Client = Client()

    def test_post(self):
        data = {
            "model": "R2",
            "version": "D2",
            "created": "2022-12-31 23:59:59"
        }
        json_data = json.dumps(data)

        response = self.client.post(
            reverse('post_json'), json_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content, {'message': 'Data received successfully'}
        )
