from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor-specialty/', views.doctor_specialty, name='doctor_specialty'),
]