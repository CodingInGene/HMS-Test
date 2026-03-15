from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Specialization, TimeSlot, Appointment
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from notifications.utils import send_email, create_event

# Create your views here.
@login_required
def home(request):
    doctors = Doctor.objects.all()
    specializations = Specialization.objects.all()

    time_slots = None
    appointments = None

    if request.user.role == "doctor":    # If doctor only then search
        doctor_lookup = get_object_or_404(Doctor, user=request.user)
        time_slots = TimeSlot.objects.filter(doctor=doctor_lookup)
        appointments = Appointment.objects.filter(appointment_slot__doctor = doctor_lookup)     # For doctors
    else:
        patient_lookup = get_object_or_404(Patient, user=request.user)
        appointments = Appointment.objects.filter(patient=patient_lookup)       # For patients

    data = {
        "doctors":doctors,
        "specializations":specializations,
        "timings":time_slots,
        "appointments":appointments,
    }

    return render(request, "home.html", data)


# Create
def create_timeslot(request):
    if request.method == "POST":
        start = request.POST.get("starttime")
        end = request.POST.get("endtime")
        print(start, end)

        try:
            doctor_lookup = get_object_or_404(Doctor, user=request.user)
            timeslot = TimeSlot.objects.create(doctor=doctor_lookup, time_start=start, time_end=end)
        except Exception as e:
            print("Error while create time slot-", e)
            messages.error(request, "Something went wrong")

    return redirect("/")

def create_appointment(request):
    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        slot_id = request.POST.get("slot_id")

        try:
            slot_lookup = get_object_or_404(TimeSlot, id=slot_id)
            patient_lookup = get_object_or_404(Patient, user=request.user)

            conflict = Appointment.objects.filter(patient=patient_lookup, appointment_slot=slot_lookup).exists()

            if not conflict:
                # Create booking on db
                new_booking = Appointment.objects.create(patient=patient_lookup, appointment_slot=slot_lookup)
                new_booking.save()

                # Send booking email to Doctor
                body = f'''Hi {new_booking.appointment_slot.doctor.user.first_name}, 
                You have an appointment with patient {request.user.first_name} {request.user.last_name},
                in the time slot - {new_booking.appointment_slot.time_start} - {new_booking.appointment_slot.time_start}.'''

                doctor_email = new_booking.appointment_slot.doctor.user.email
                doctor_name = new_booking.appointment_slot.doctor.user.first_name

                send_email(purpose="appointment", recipient_email=doctor_email, recipient_name=doctor_name, body=body)

                # Send booking email to Patient
                body = f'''Hi {request.user.first_name}, 
                You have an appointment with Dr. {new_booking.appointment_slot.doctor.user.first_name} {new_booking.appointment_slot.doctor.user.last_name},
                in the time slot - {new_booking.appointment_slot.time_start} - {new_booking.appointment_slot.time_end}.'''

                send_email(purpose="appointment", recipient_email=request.user.email, recipient_name=request.user.first_name, body=body)

                # Create calender event
                create_event(
                    doctor_name=doctor_name,
                    patient_name=request.user.first_name,
                    doctor_email=doctor_email,
                    patient_email=request.user.email,
                    start_time=new_booking.appointment_slot.time_start,
                    end_time=new_booking.appointment_slot.time_end
                    )

        except Exception as e:
            print("Error while create appointment-", e)
            messages.error(request, "Something went wrong")

    return redirect("/")


# Updation
def update_specialization(request):
    if request.method == "POST":
        try:
            sp = request.POST.get("specialization")

            # Change doctors specialization
            sp_lookup = get_object_or_404(Specialization, name=sp)
            doctor_lookup = get_object_or_404(Doctor, user=request.user)
            doctor_lookup.specialization = sp_lookup

            doctor_lookup.save()

        except Exception as e:
            print("Error in specialization update-", e)
            messages.error(request, "Something went wrong")
    
    return redirect("/")

def update_timeslot(request):
    if request.method == "POST":
        id_ = request.POST.get("id")
        start = datetime.strptime(request.POST.get('starttime'), '%H:%M').time()
        end = datetime.strptime(request.POST.get('endtime'), '%H:%M').time()

        if start >= end:
            messages.error(request, "Timings are not valid")
            return redirect("/")

        # Validate timing
        doctor_lookup = Doctor.objects.get(user=request.user)
        slot_conflict = TimeSlot.objects.filter(doctor=doctor_lookup).filter(
            Q(time_start=start) | Q(time_end=end)).exclude(id=id_).exists()

        if not slot_conflict:
            try:
                timelookup = get_object_or_404(TimeSlot, id=id_)
                timelookup.time_start = start
                timelookup.time_end = end
                timelookup.save()
            except Exception as e:
                print("Error in timeslot update-", e)
                messages.error(request, "Something went wrong")

    return redirect("/")


# Delete
def del_appointment(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        patient = get_object_or_404(Patient, user=request.user)

        try:
            # Cancel appointment
            appointment = get_object_or_404(Appointment, pk=appointment_id, patient=patient)
            appointment.delete()

        except Exception as e:
                print("Error in appointment cancellation-", e)
                messages.error(request, "Something went wrong")

    return redirect("/")

def delete_timeslot(request):
    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        try:
            doctor_lookup = get_object_or_404(Doctor, user=request.user)
            # Filtering using user, id for security
            slot = get_object_or_404(TimeSlot, pk=slot_id, doctor=doctor_lookup)
            slot.delete()
            
        except Exception as e:
            print("Error deleting slot:", e)
            messages.error(request, "Something went wrong")
    return redirect("/")