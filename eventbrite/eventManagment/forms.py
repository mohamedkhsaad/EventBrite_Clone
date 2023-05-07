from django import forms

class Password_Form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)