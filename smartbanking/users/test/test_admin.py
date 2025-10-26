from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, KYC
from django.core.files.uploadedfile import SimpleUploadedFile

class AdminAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='adminuser', password='Adminpass123!', email='admin123@gmail.com',role='admin')
        self.customer = User.objects.create_user(username='customer1', password='Custpass123!',email='customer123@gmail.com', role='customer')
        self.admin_users_url = reverse('view_all_users')
        self.admin_kyc_url = reverse('admin_verify')

    def test_admin_users_access_requires_admin(self):
        self.client.login(username='customer1', password='Custpass123!')
        response = self.client.get(self.admin_users_url)
        self.assertNotEqual(response.status_code, 302)

    def test_admin_can_view_all_users(self):
        self.client.login(username='adminuser', password='Adminpass123!')
        response = self.client.get(self.admin_users_url)
        self.assertContains(response, 'customer1')
        self.assertContains(response, 'adminuser')

    def test_admin_can_view_kyc_submissions(self):
        self.client.login(username='adminuser', password='Adminpass123!')
        test_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        KYC.objects.create(user=self.customer, document=test_image)
        response = self.client.get(self.admin_kyc_url)
        self.assertContains(response, 'customer1')
