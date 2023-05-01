from django.db import models
from eventbrite.settings import *
from user.models import *
from django.urls import reverse
from event.models import event
from django.core.exceptions import ValidationError



class Publish_Info(models.Model):
    ID = models.IntegerField()
    Event_ID = models.IntegerField()
    Event_Status_Choices = (
        ('Public', 'Public'),
        ('Private', 'Private')
    )
    Event_Status = models.CharField(max_length=7, choices=Event_Status_Choices)
    Audience_Link = models.CharField(max_length=50, default='', editable= False)
    Audience_Password = models.CharField(max_length=50, blank=True)
    Keep_Private = models.BooleanField(default=False)
    Publication_Date = models.DateField(null=False, blank=True)
 
    def default_audience_link(self):
        return 'https://127.0.0.1:8080' + reverse('event-list-by-ID', kwargs={'event_ID': self.Event_ID})
    def __str__(self):
        return f"{self.ID}: {self.Audience_Link}"

    def save(self, *args, **kwargs):
        if not self.Audience_Link:
            self.Audience_Link = self.default_audience_link()
        super().save(*args, **kwargs)

