from django import forms
from .models import event

class ImageForm(forms.ModelForm):
    class Meta:
        model = event
        fields = ['ID', 'User_id', 'Title', 'organizer', 'Summery', 'Description', 'type', 'category_name',
                  'sub_Category', 'venue_name', 'ST_DATE', 'END_DATE', 'ST_TIME', 'END_TIME', 'online', 'CAPACITY',
                  'PASSWORD', 'STATUS', 'image']
