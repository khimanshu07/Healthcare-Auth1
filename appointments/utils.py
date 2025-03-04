from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from .models import Appointment
import datetime
from django.db.models import Q


# Define time ranges for slots
TIME_RANGES = [
    ("09:00", "12:00"),  # Morning range
    ("14:00", "17:00"),  # Afternoon range
    ("18:00", "19:30"),  # Evening range
]


# Define Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_credentials(request):
    """Get or create Google Calendar API credentials."""
    creds = None
    if 'google_credentials' in request.session:
        creds = Credentials.from_authorized_user_info(request.session['google_credentials'], SCOPES)

    # If credentials are expired or invalid, refresh them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials in the session
        request.session['google_credentials'] = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes,
        }

    return creds

def create_google_calendar_event(request, appointment):
    """Create a Google Calendar event for the appointment."""
    creds = get_google_calendar_credentials(request)
    service = build('calendar', 'v3', credentials=creds)

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


def generate_time_slots():
    """Generate 45-minute time slots within the defined ranges."""
    slots = []
    for start, end in TIME_RANGES:
        current_time = datetime.datetime.strptime(start, "%H:%M")
        end_time = datetime.datetime.strptime(end, "%H:%M")
        while current_time <= end_time:
            slots.append(current_time.strftime("%H:%M"))
            current_time += datetime.timedelta(minutes=45)
    return slots

def get_available_time_slots(doctor, appointment_date):
    """
    Get available 45-minute time slots for a doctor on a specific date.
    This function checks for existing appointments and filters out booked slots.
    """
    # Get all appointments for the doctor on the selected date
    existing_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
    )

    # Convert existing appointments to a set of booked slots
    booked_slots = set()
    for appointment in existing_appointments:
        start_time = appointment.start_time.strftime("%H:%M")
        end_time = appointment.end_time.strftime("%H:%M")
        booked_slots.add(start_time)
        booked_slots.add(end_time)

    # Generate all possible 45-minute slots
    all_slots = generate_time_slots()

    # Filter out booked slots
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    # Debug: Print available slots
    print("Available Slots:", available_slots)

    return available_slots