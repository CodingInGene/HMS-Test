from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path('', views.home, name="homepage"),

    # Create
    path('doctor/createtimeslot', views.create_timeslot, name="create_timeslot"),
    path('appointment/create', views.create_appointment, name="create_appointment"),

    # Update
    path('doctor/updatespecialization/', views.update_specialization, name="update_specialization"),
    path('doctor/updatetimeslot/', views.update_timeslot, name="update_timeslot"),

    # Delete
    path('patient/delappointment/', views.del_appointment, name="del_appointment"),
    path('doctor/deltimeslot/', views.delete_timeslot, name="delete_timeslot"),
]