from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, DoctorSpecialtyForm
from blog.models import Category

def index(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
    return render(request, 'users/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_redirect')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def login_redirect(request):
    if request.user.user_type == 'patient':
        return redirect('patient_dashboard')
    elif request.user.user_type == 'doctor':
        if request.user.is_doctor_without_specialty():
            return redirect('doctor_specialty')
        else:
            return redirect('doctor_dashboard')
    else:
        # Handle unexpected user types (e.g., admins or other roles)
        return redirect('index')
    
@login_required
def doctor_specialty(request):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        form = DoctorSpecialtyForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()  # Save many-to-many data (specialties)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSpecialtyForm(instance=request.user)
    
    return render(request, 'users/doctor_specialty.html', {'form': form})

@login_required
def patient_dashboard(request):
    categories = Category.objects.all()
    return render(request, 'users/patient_dashboard.html', {'categories': categories})

@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor' or request.user.is_doctor_without_specialty():
        return redirect('login_redirect')
    
    return render(request, 'users/doctor_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('index')
