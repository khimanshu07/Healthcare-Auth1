from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = (
        'id', 
        'patient', 
        'doctor', 
        'specialty', 
        'appointment_date', 
        'start_time', 
        'end_time'
    )
    
    # Fields to use for searching
    search_fields = (
        'patient__first_name', 
        'patient__last_name', 
        'doctor__first_name', 
        'doctor__last_name', 
        'specialty'
    )
    
    # Fields to filter by in the admin
    list_filter = (
        'appointment_date', 
        'specialty', 
        'doctor'
    )
    
    # Make certain fields readonly in the admin interface
    readonly_fields = (
        'google_calendar_event_id',
    )

    # Customize the detail view
    fieldsets = (
        ('Appointment Details', {
            'fields': (
                'patient', 
                'doctor', 
                'specialty', 
                'appointment_date', 
                'start_time', 
                'end_time'
            )
        }),
        ('Additional Information', {
            'fields': (
                'google_calendar_event_id',
            ),
            'classes': ('collapse',)
        })
    )

# Register the model with the custom admin class
admin.site.register(Appointment, AppointmentAdmin)