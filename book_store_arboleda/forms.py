from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class Createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1', 'password2'] 
        
class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'email']
        
class Createcartform(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'books']
    
    customer = forms.ModelChoiceField(queryset=User.objects.all())
    

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['date', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['date','status_revision']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        

class Createbookform(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price']

class CreateStockForm(ModelForm):

    
    class Meta:
        model = Stock
        fields = ['total_copies', 'copies_in_stock']

        
class CreateAuthorForm(ModelForm):
    name = forms.CharField(required=False)
    class Meta:

        model=Author
        fields=['name']
        labels = {
            'name': 'Author name'
        }