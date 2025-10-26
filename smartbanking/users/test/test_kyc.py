from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, KYC
from django.core.files.uploadedfile import SimpleUploadedFile

class KYCTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='gane@543.com',password='Testpass123!', role='customer')
        self.kyc_url = reverse('kyc_submit')

    def test_kyc_access_requires_login(self):
        response = self.client.get(self.kyc_url)
        self.assertNotEqual(response.status_code, 200) 

    def test_kyc_submission(self):
        self.client.login(username='testuser', password='Testpass123!')
        test_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(self.kyc_url, {'document': test_image}, follow=True)
        self.assertContains(response, "KYC submitted successfully")
      