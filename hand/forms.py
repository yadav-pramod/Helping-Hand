from django import forms
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.contrib.auth.forms import UserCreationForm


class myform(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField( max_length=20)
    last_name=forms.CharField( max_length=20)
    
        

    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']


