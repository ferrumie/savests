from django import forms


class SendEmailForm(forms.Form):
    ''' Email sending form'''
    subject = forms.CharField(
                    widget=forms.TextInput(attrs={'placeholder': ('Subject')}))
    message = forms.CharField(widget=forms.Textarea)
    