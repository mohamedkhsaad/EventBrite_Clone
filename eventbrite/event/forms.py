from django import forms
from .models import event

class ImageForm(forms.ModelForm):
    class Meta:
        model = event
        fields = '__all__'
