from django.db import models
import uuid

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Specialization(BaseModel):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


class Doctor(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_to_doctor')
    specialization = models.ForeignKey(to=Specialization, on_delete=models.CASCADE, default='', blank=True, null=True)

    def __str__(self):
        return self.user.first_name

    def available_slots(self):
        return self.doctor_to_timeslot.filter(timeslot_to_appointment__isnull=True)


class TimeSlot(BaseModel):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE, related_name='doctor_to_timeslot')
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return self.doctor.user.first_name + " " + str(self.time_start) + "-" + str(self.time_end)

class Patient(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_to_patient')

class Appointment(BaseModel):
    patient = models.ForeignKey(to=Patient, on_delete=models.CASCADE, related_name='patient_to_appointment')
    appointment_slot = models.OneToOneField(to=TimeSlot, on_delete=models.CASCADE, related_name='timeslot_to_appointment')