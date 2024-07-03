from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import random

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=30, blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        self.save()


class UserProfile(models.Model):
    profile_pic = models.ImageField(
        upload_to='profile_pic', default='default.png')
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"


class TranslationRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    source_text = models.TextField(blank=True, null=True)
    translated_text = models.TextField(blank=True, null=True)
    source_language = models.CharField(max_length=50, blank=True, null=True)
    target_language = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.source_text[:20]}... to {self.target_language}"


class TextToSpeechRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    audio_file = models.FileField(upload_to='text_to_speech')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text[:20]}... in {self.language}"


class SpeechToTextRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='speech_to_text')
    language = models.CharField(max_length=50, blank=True, null=True)
    transcribed_text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transcription in {self.language}"


class SavedPhrase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phrase = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phrase[:20]
