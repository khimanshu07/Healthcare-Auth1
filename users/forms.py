from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Specialty

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    address_line1 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    state = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    pincode = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'user_type',
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'address_line1',
            'city',
            'state',
            'pincode',
            'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class DoctorSpecialtyForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=Specialty.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selection
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['specialties']
        widgets = {
            'specialties': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }