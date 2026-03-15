from django.contrib import admin
from .models import Doctor, Patient, Specialization, Appointment, TimeSlot

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Specialization)
admin.site.register(Appointment)
admin.site.register(TimeSlot)