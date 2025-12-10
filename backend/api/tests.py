from django.test import TestCase
from django.contrib.auth.models import User

class SimpleAuthTest(TestCase):
    def test_register_and_login(self):
        res = self.client.post('/api/register/', {'username':'tuser','password':'123456'})
        self.assertEqual(res.status_code, 200)
        token = res.json().get('token')
        self.assertTrue(token)
        res2 = self.client.post('/api/login/', {'username':'tuser','password':'123456'})
        self.assertEqual(res2.status_code, 200)
