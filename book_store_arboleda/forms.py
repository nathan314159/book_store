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

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            customer = None

        if customer:
            # If customer with the email already exists, update the existing customer
            customer.first_name = self.cleaned_data.get('first_name')
            customer.last_name = self.cleaned_data.get('last_name')
            customer.phone_number = self.cleaned_data.get('phone_number')
            if commit:
                customer.save()
            return customer
        else:
            # If customer with the email doesn't exist, create a new customer
            return super().save(commit=commit)
        
class Createcartform(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'books']
    
    customer = forms.ModelChoiceField(queryset=User.objects.all())
    

class PaymentForm(ModelForm):
    
    class Meta:
        model = Payment
        fields = ['payment_method']

        
# class InvoiceForm(ModelForm):
#     class Meta:
#         model = Invoice
#         fields = ['status_revision']

        

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