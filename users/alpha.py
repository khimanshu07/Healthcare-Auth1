from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    pincode = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                 'user_type', 'profile_picture', 'address_line1', 'city', 'state', 'pincode')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data