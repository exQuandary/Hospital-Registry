from django.db import models
from django.db import models
from django.utils import timezone

# Create your models here.


class Patient(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    phone = models.CharField(max_length=20)
    insurance = models.CharField(max_length=40)


class Provider(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    license = models.CharField(max_length=9)
    department = models.CharField(max_length=30)


class Nurse(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    license = models.CharField(maxlength=9)


class Section(models.Model):
    STATUS_CHOICES = (
        ('inp', 'Inpatient'),
        ('outp', 'Outpatient'),
        ('ER', 'Emergency Room'),
        ('OR', 'Operating Room'),
        ('MA', 'Maternity')
    )

    status = models.CharField(
        max_length=5, choices=SECTION_CHOICES, primary_key=True)
    charge = models.DecimalField(max_digits=8, decimale_places=2)


class Visit(models.Model):
    reason = models.CharField(max_length=50)
    admit_time = models.DateTimeField(default=timezone.now)
    discharge_time = models.DateTimeField(null=True, blank=True)
    patient_id = models.ForeignKey(Patient)
    nurse_id = models.ForeignKey(Nurse)
    provider_id = models.ForeignKey(Provider)
    status = models.ForeignKey(Section)


class Bill(models.Model):
    amount = models.DecimalField(max_digits=8, decimale_places=2)
    status = models.ForeignKey(Section)
    paid = models.BooleanField(default=False)
