Users -
    1. name
    2. email
    3. number
    4. roles

Doctors -
    1. Specialization foreign Many-Many
    2. Users - foreign

Patients
    1. Users - Foreign
    2. booked_slots

TimeSlots  (This is only to store doctor's time slots)
    1. Doctors - Foreign
    2. time

Specialization
    1. Name

Appointment -
    1. Doctors - Foreign
    2. Patients - Foreign
    3. time_slot - Foreign TimeSlots (1-1)