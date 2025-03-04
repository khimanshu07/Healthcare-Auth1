from django.db import models
from users.models import CustomUser
import datetime

class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    specialty = models.CharField(max_length=100)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    google_calendar_event_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate end_time as 45 minutes after start_time
        if self.start_time and not self.end_time:
            start_datetime = datetime.datetime.combine(datetime.date.today(), self.start_time)
            self.end_time = (start_datetime + datetime.timedelta(minutes=45)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment: {self.patient.first_name} with {self.doctor.first_name} on {self.appointment_date}"