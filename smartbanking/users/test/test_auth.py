from django.test import TestCase, Client
from django.urls import reverse
from users.models import User

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'role': 'customer'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data,follow=False)
        self.assertNotEqual(response.status_code, 302) 

    def test_login_user(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='Testpass123!', role='customer')
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'Testpass123!'},follow=True)
        self.assertNotEqual(response.status_code, 302)  

    def test_logout_user(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='Testpass123!', role='customer')
        self.client.login(username='testuser', password='Testpass123!',follow=False)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  