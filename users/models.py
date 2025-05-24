
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
# Phone number validator
phone_validator = RegexValidator(
    regex=r'^(0[1-9]{1})\d{8}$',
    message="Phone number must be entered in the format: '0789776655'. It should be 10 digits long.")    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (('kiongozi', 'Kiongozi'), ('mwananchi', 'Mwananchi'),)
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'),)

    f_name = models.CharField(max_length=30)
    m_name = models.CharField(max_length=30, blank=True, null=True)
    l_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    phone_no = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='mwananchi')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['f_name', 'l_name', 'location', 'date_of_birth', 'phone_no']

    def __str__(self):
        return self.email

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='announcements/images/', blank=True, null=True)
    file = models.FileField(upload_to='announcements/files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title