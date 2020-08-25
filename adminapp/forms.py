from .models import customUser
from django.contrib.auth.models import User
from django import forms



class SendEmailForm(forms.Form):
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
   # users = forms.ModelMultipleChoiceField(label="To", queryset=User.objects.all(), widget=forms.SelectMultiple())