from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import Appointment
from users.models import Specialty
from .forms import AppointmentForm
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
from .utils import create_google_calendar_event

@login_required
def list_doctors(request):
    if request.user.user_type != 'patient':
        return redirect('doctor_dashboard')
    
    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'appointments/list_doctors.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    if request.user.user_type != 'patient':
        return redirect('patient_dashboard')

    doctor = get_object_or_404(CustomUser, id=doctor_id)

    if request.method == 'POST':
        # Create the form with POST data and doctor
        form = AppointmentForm(request.POST, doctor=doctor)
        
        if form.is_valid():
            # Create appointment instance
            appointment = form.save(commit=False)
            
            # Set patient and doctor
            appointment.patient = request.user
            appointment.doctor = doctor
            
            # Set specialty from form data
            appointment.specialty = request.POST.get('specialty')
            
            # Set start and end times from cleaned data
            appointment.start_time = form.cleaned_data['start_time']
            appointment.end_time = form.cleaned_data['end_time']
            
            # Save the appointment
            appointment.save()

            return redirect('appointment_confirmation', appointment_id=appointment.id)
        else:
            # If form is not valid, print out errors for debugging
            print("Form Errors:", form.errors)
    else:
        # For GET request, initialize the form with the doctor
        form = AppointmentForm(doctor=doctor)

    return render(request, 'appointments/book_appointment.html', {
        'form': form, 
        'doctor': doctor
    })

@login_required
def appointment_confirmation(request, appointment_id):
    """Display appointment confirmation details."""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Ensure the patient can only view their own appointments
    if request.user != appointment.patient:
        return redirect('patient_dashboard')
    
    return render(request, 'appointments/appointment_confirmation.html', {'appointment': appointment})

@login_required
def doctor_appointments(request):
    """Display all appointments for the logged-in doctor."""
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    
    # Fetch all appointments for the logged-in doctor
    appointments = Appointment.objects.filter(doctor=request.user).order_by('appointment_date', 'start_time')
    
    return render(request, 'appointments/doctor_appointments.html', {'appointments': appointments})

@login_required
def view_appointment(request, appointment_id):
    """Display details of a specific appointment."""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Ensure the logged-in doctor can only view their own appointments
    if request.user != appointment.doctor:
        return redirect('doctor_dashboard')
    
    return render(request, 'appointments/view_appointment.html', {'appointment': appointment})


def create_google_calendar_event(request, appointment):
    # Load credentials from the session or database
    credentials = Credentials.from_authorized_user_info(request.session.get('google_credentials'))
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
    
    service = build('calendar', 'v3', credentials=credentials)
    
    event = {
        'summary': f'Appointment with {appointment.patient.first_name}',
        'description': f'Appointment for {appointment.specialty}',
        'start': {
            'dateTime': f'{appointment.appointment_date}T{appointment.start_time}:00',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': f'{appointment.appointment_date}T{appointment.end_time}:00',
            'timeZone': 'UTC',
        },
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('id')


def google_calendar_redirect(request):
    """Handle the OAuth redirect from Google."""
    return redirect('list_doctors')