
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Announcement
from .models import Document
from django.contrib.auth.models import User

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'f_name', 'm_name', 'l_name', 'email', 'location',
            'date_of_birth', 'gender', 'phone_no', 'role'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=CustomUser.GENDER_CHOICES),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].disabled = True

    def clean_role(self):
        return self.instance.role

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = (('kiongozi', 'Kiongozi'), ('mwananchi', 'Mwananchi'),)
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'),)

    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Nafasi')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Jinsia')

    class Meta:
        model = CustomUser
        fields = ['f_name', 'm_name', 'l_name', 'email', 'location',
                  'date_of_birth', 'gender', 'phone_no', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.gender = self.cleaned_data['gender']
        if commit:
            user.save()
        return user

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'file']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']