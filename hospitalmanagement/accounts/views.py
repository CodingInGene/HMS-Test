from django.shortcuts import render, redirect
from accounts.forms import UserRegistration
from django.contrib.auth import login
from core.models import Doctor, Patient
from notifications.utils import send_email

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()

            # If doctor
            if user.role == "doctor":
                new_doctor = Doctor.objects.create(user=user)
                new_doctor.save()
            
            # If patient
            if user.role == "patient":
                new_patient = Patient.objects.create(user=user)
                new_patient.save()

            login(request, user)

            # Send signup email
            body = f"Hi {user.first_name}, Welcome to the team"
            send_email(purpose="signup", recipient_email=user.email, recipient_name=user.first_name, body=body)

            return redirect("core:homepage")
    else:
        form = UserRegistration()

    data = {
        "form":form
    }

    return render(request, "registration/register.html", data)
