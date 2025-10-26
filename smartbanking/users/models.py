from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import os

def kyc_upload_path(instance, filename):
    return os.path.join('kyc_documents', str(instance.user.id), filename)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='customer'):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, username, email, password=None):
        return self.create_user(username, email, password, role='admin')

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class KYC(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to=kyc_upload_path)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

