from django import forms
from .models import Appointment
from .utils import get_available_time_slots, generate_time_slots
from django.core.exceptions import ValidationError
import datetime

class AppointmentForm(forms.ModelForm):
    time_slot = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'time_slot']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)

        # Populate time_slot choices dynamically based on the doctor
        if self.doctor:
            # By default, use today's date if no specific date is provided
            today = datetime.date.today()
            available_slots = get_available_time_slots(self.doctor, today)
            self.fields['time_slot'].choices = [(slot, slot) for slot in available_slots]
        else:
            # Default to all slots if no doctor is provided
            all_slots = generate_time_slots()
            self.fields['time_slot'].choices = [(slot, slot) for slot in all_slots]

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        time_slot = cleaned_data.get('time_slot')
        
        # Get the specialty from the form data
        specialty = self.data.get('specialty')
        
        # Get the current date and time
        now = datetime.datetime.now()
        current_date = now.date()
        current_time = now.time()

        # Validate appointment date
        if not appointment_date:
            raise ValidationError("Appointment date is required.")
        
        if appointment_date < current_date:
            raise ValidationError("Appointment date cannot be in the past.")

        # Validate time slot
        if not time_slot:
            raise ValidationError("Time slot is required.")

        # Parse the selected time slot
        start_time = datetime.datetime.strptime(time_slot, "%H:%M").time()
        end_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=45)).time()

        # Validate appointment time if the date is today
        if appointment_date == current_date:
            # Check if the selected time slot is in the past
            if start_time < current_time:
                raise ValidationError("You cannot select a time slot that has already passed for today.")

        # Check for overlapping appointments
        if self.doctor:
            overlapping_appointments = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=appointment_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(id=self.instance.id if self.instance else None)

            if overlapping_appointments.exists():
                raise ValidationError("This time slot is already booked. Please choose another time.")

        # Add processed data to cleaned_data
        cleaned_data['start_time'] = start_time
        cleaned_data['end_time'] = end_time
        
        # Ensure specialty is added to cleaned_data
        if not specialty:
            raise ValidationError("Specialty is required.")
        
        cleaned_data['specialty'] = specialty

        return cleaned_data