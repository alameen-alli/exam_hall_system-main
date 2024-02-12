from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, Student, Invigilator
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from PIL import Image
from exam_hall_system import settings

from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

        
class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "middle_name", 
                                                 "last_name", "date_of_birth", 'level')
        
        
class InvigilatorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Invigilator
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "middle_name", 
                                                 "last_name", "date_of_birth")
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            # Check if the uploaded file is an image
            with Image.open(avatar) as img:
                img.verify()
        except (IOError, SyntaxError) as e:
            raise forms.ValidationError("Not a valid image file. Please upload a valid image.")

        return avatar

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)

        if commit:
            profile.save()

        return profile
    
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'date_of_birth']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
