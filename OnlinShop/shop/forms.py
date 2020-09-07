from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
quantity_choices=[(i,str(i)) for i in range(1,21) ]
class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1", "password2"]

class Client_Form(forms.ModelForm):
    class Meta:
        model=models.Client
        fields=['phone','email']
class CartAdd(forms.Form):
    quantity=forms.TypedChoiceField(choices=quantity_choices,coerce=int)
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'
