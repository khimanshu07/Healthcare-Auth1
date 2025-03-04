from django.shortcuts import redirect
from django.urls import reverse

class DoctorSpecialtyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.user_type == 'doctor' and request.user.is_doctor_without_specialty():
            if request.path != reverse('doctor_specialty'):
                return redirect('doctor_specialty')
        
        response = self.get_response(request)
        return response