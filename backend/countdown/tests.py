from django.test import TestCase, Client
from django.urls import reverse
from .models import Countdown
from datetime import datetime, timedelta
import time

class CountdownTestCase(TestCase):
    def test_subtraction(self):
        self.assertEqual(2 - 2, 0)

    def setUp(self):
        self.client = Client()
        # Set up initial data for tests with Unix timestamp
        target_time = int(time.mktime((datetime.now() + timedelta(days=1)).timetuple()))
        Countdown.objects.create(target_time=target_time)

    def test_countdown_endpoint(self):
        response = self.client.get('/countdown/')
        self.assertEqual(response.status_code, 200)
        if response['Content-Type'] == 'application/json':
            self.assertIn('countdown', response.json())
        else:
            self.assertIn('Countdown app is working!', response.content.decode())  # Check for specific HTML content

    def test_get_countdown_endpoint(self):
        url = '/countdown/get/'
        response = self.client.get(url)
        if response.status_code != 200:
            self.fail(f'Fetched URL: {url}, Status Code: {response.status_code}, Content: {response.content.decode()}')
        self.assertEqual(response.status_code, 200)
        if response['Content-Type'] == 'application/json':
            self.assertIn('target_time', response.json())
        else:
            self.fail(f'Response content is not JSON: {response.content.decode()}')

    def test_set_countdown_endpoint(self):
        url = '/countdown/set/'
        target_time = int(time.mktime((datetime.now() + timedelta(days=1)).timetuple()))
        response = self.client.post(url, {'target_time': target_time}, content_type='application/json')
        if response.status_code != 200:
            self.fail(f'Fetched URL: {url}, Status Code: {response.status_code}, Content: {response.content.decode()}')
        self.assertEqual(response.status_code, 200)
        if response['Content-Type'] == 'application/json':
            self.assertIn('success', response.json())
        else:
            self.fail(f'Response content is not JSON: {response.content.decode()}')
