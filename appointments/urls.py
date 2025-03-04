from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    path('doctor-appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('view-appointment/<int:appointment_id>/', views.view_appointment, name='view_appointment'),
]