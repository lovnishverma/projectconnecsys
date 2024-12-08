from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    WORK_PROFILE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Working Professional', 'Working Professional'),
        ('Unemployed', 'Unemployed'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    university_college = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    currently_pursuing = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    work_profile = models.CharField(max_length=50, choices=WORK_PROFILE_CHOICES)

    def __str__(self):
        return self.full_name


# avr Bootcamp Certificates
class avrBootcampCertificates(models.Model):
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    course_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    issue_date = models.DateField(null=True, blank=True)
    qr_url = models.URLField(null=True, blank=True)  # QR code URL, can be null
    cert_no = models.CharField(max_length=100, null=True, blank=True)  # Certificate number, can be null
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.start_date}"


class CertificateAttributes(models.Model):
    attribute_name = models.CharField(max_length=255)
    pos_x = models.IntegerField()  # Position X coordinate
    pos_y = models.IntegerField()  # Position Y coordinate
    x_offset = models.IntegerField()  # X offset value
    font_color = models.CharField(max_length=7)
    font_size = models.IntegerField()
    center = models.BooleanField(default=False)  # Center alignment, True or False

    def __str__(self):
        return f"{self.attribute_name}"
