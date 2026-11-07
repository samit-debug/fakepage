from django.db import models
import random
from django.utils import timezone
from datetime import timedelta

class PlainTextUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Stores raw, unhashed password
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code

    def is_otp_valid(self):
        # OTP expires after 5 minutes
        if self.otp_created_at:
            return timezone.now() < self.otp_created_at + timedelta(minutes=5)
        return False

    def __str__(self):
        return self.email
