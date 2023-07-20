# forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture')

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')

        # Check if a file is uploaded for the profile picture field
        if not profile_picture:
            # Set the default profile picture path if no file is uploaded
            profile_picture = 'profile_pics/default_profile_picture.png'
        return profile_picture

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']