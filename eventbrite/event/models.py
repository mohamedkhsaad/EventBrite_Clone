from django.db import models
from eventbrite.settings import *
from user.models import *
from django.urls import reverse
import random
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

from django.http import JsonResponse


CATEGORY_CHOICES = (
    ('Category', 'Category'),
    ('Auto, Boat & Air', 'Auto, Boat & Air'),
    ('Business & Professional', 'Business & Professional'),
    ('Charity & Causes', 'Charity & Causes'),
    ('Community & Culture', 'Community & Culture'),
    ('Family & Education', 'Family & Education'),
    ('Fashion & Beauty', 'Fashion & Beauty'),
    ('Film, Media & Entertainment', 'Film, Media & Entertainment'),
    ('Food & Drink', 'Food & Drink'),
    ('Government & Politics', 'Government & Politics'),
    ('Health & Wellness', 'Health & Wellness'),
    ('Hobbies & Special Interest', 'Hobbies & Special Interest'),
    ('Home & Lifestyle', 'Home & Lifestyle'),
    ('Music', 'Music'),
    ('Performing & Visual Arts', 'Performing & Visual Arts'),
    ('Religion & Spitituality', 'Religion & Spitituality'),
    ('School Activities', 'School Activities'),
    ('Science & Technology', 'Science & Technology'),
    ('Seasonal & Holiday', 'Seasonal & Holiday'),
    ('Sports & Fitness', 'Sports & Fitness'),
    ('Travel & Outdoor', 'Travel & Outdoor'),
    ('Other', 'Other'),
)
TYPE_CHOICES = [
    ('Type', 'Type'),
    ('Appearance or Singing', 'Appearance or Singing'),
    ('Attraction', 'Attraction'),
    ('Camp, Trip, or Retreat', 'Camp, Trip, or Retreat'),
    ('Class, Training, or Workshop', 'Class, Training, or Workshop'),
    ('Concert or Performance', 'Concert or Performance'),
    ('Conference', 'Conference'),
    ('Convention', 'Convention'),
    ('Dinner or Gala', 'Dinner or Gala'),
    ('Festival or fair', 'Festival or fair'),
    ('Game or Competition', 'Game or Competition'),
    ('Meeting or Networking Event', 'Meeting or Networking Event'),
    ('Party or Social Gathering', 'Party or Social Gathering'),
    ('Race or Endurance Event', 'Race or Endurance Event'),
    ('Rally', 'Rally'),
    ('Screening', 'Screening'),
    ('Seminar or Talk', 'Seminar or Talk'),
    ('Tour', 'Tour'),
    ('Tournment', 'Tournment'),
    ('Tradeshow, Consumer Show, or Expo', 'Tradeshow, Consumer Show, or Expo'),
    ('Other', 'Other'),
]
Online_choises = (
    ('True', 'True'),
    ('False', 'False')
)
STATUS_choises = (
    ('Draft', 'Draft'),
    ('Live', 'Live'),
    ('Past', 'Past')
)
Publish_choises = (
    ('Private', 'Private'),
    ('Public', 'Public'),
)


def generate_unique_id():
    while True:
        # Generate a random integer between 1 and 99999999
        new_id = random.randint(1, 99999999)
        # Check if an event with this ID already exists in the database
        if not event.objects.filter(ID=new_id).exists():
            return new_id


class UserInterest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='interests')
    User_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=255)
    sub_Category = models.CharField(max_length=255)

    def __str__(self):
        return self.User_id

class event(models.Model):
    """
    Model representing an event.
    """
    ID = models.IntegerField(unique=True, default=generate_unique_id)
    User_id = models.IntegerField(blank=True, null=True)
    Title = models.CharField(max_length=50)
    organizer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    organizer = models.CharField(max_length=50)
    Summery = models.CharField(max_length=500, null=True)
    Description = models.CharField(max_length=500, null=True)
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default='Type')
    category_name = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='Category')
    sub_Category = models.CharField(max_length=20,null=True,blank=True)
    venue_name = models.CharField(max_length=20,blank=True)
    ST_DATE = models.DateField()
    END_DATE = models.DateField()
    ST_TIME = models.TimeField()
    END_TIME = models.TimeField()
    online = models.CharField(max_length=5, choices=Online_choises)
    CAPACITY = models.IntegerField()
    STATUS = models.CharField(max_length=5,choices=STATUS_choises)
    # Publish = models.CharField(max_length=10, choices=Publish_choises)
    # PASSWORD = models.CharField(max_length=10, null=True)
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        """String for representing the Model object."""
        return self.Title


class category(models.Model):
    """
    Model representing an event category.
    """

    ID = models.IntegerField()
    Name = models.CharField(max_length=20)
    EVENT_ID = models.IntegerField()
    SUB_CATEGORY_ID = models.IntegerField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.Name


class sub_category(models.Model):
    """
    Model representing an event sub-category.
    """

    ID = models.IntegerField()
    EVENT_ID = models.IntegerField()
    NAME = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Sub-Category"
        verbose_name_plural = "Sub-Categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.Name


class Locations(models.Model):
    """
    Model representing an event location.
    """

    ID = models.IntegerField()
    EVENT_ID = list()
    USER_ID = list()
    adress = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        """String for representing the Model object."""
        return self.address


def add_image_fields(count):
    # Add first image field as 'image'
    event.add_to_class('image', models.ImageField(
        upload_to='events/', blank=True, null=True, verbose_name='image'))
    # Add remaining image fields with field names 'image2', 'image3', ...
    for i in range(2, count+1):
        field_name = f"image{i}"
        field = models.ImageField(
            upload_to='events/', blank=True, null=True, verbose_name=field_name)
        event.add_to_class(field_name, field)


add_image_fields(10)


class EventFollower(models.Model):
    """
    Model representing a user following an event.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='event_followers')
    event = models.ForeignKey(event, on_delete=models.CASCADE,null=True,blank=True)
    followed_date = models.DateTimeField(auto_now_add=True)
    ID = models.IntegerField()


class Eventlikes(models.Model):
    """
    Model representing a user following an event.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='event_Likes')
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True)
    ID = models.IntegerField()
