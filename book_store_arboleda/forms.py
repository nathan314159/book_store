from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class Createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name', 'email','password1', 'password2'] 
 
class Createbookform(ModelForm):
    class Meta:
        model=Book
        fields='__all__'
        
class Createcartform(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['customer', 'books']
    
    customer = forms.ModelChoiceField(queryset=User.objects.all())