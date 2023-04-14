from django.db import models
from eventbrite.settings import *
from user.models import *
from django.urls import reverse

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    category_name = models.CharField(max_length=255)
    sub_Category = models.CharField(max_length=255)  
    def __str__(self):
        return f"{self.user.email} - {self.interest.category_name} - {self.interest.sub_Category}"
  

class event(models.Model):
    """
    Model representing an event.
    """
    ID = models.IntegerField(unique=True)
    User_id = models.IntegerField(blank=False)
    Title = models.CharField(max_length=50)
    organizer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organizer = models.CharField(max_length=50)
    Summery = models.CharField(max_length=500)
    Description = models.CharField(max_length=500)
    type = models.CharField(max_length=20)
    category_name = models.CharField(max_length=10)
    sub_Category = models.CharField(max_length=20)
    venue_name = models.CharField(max_length=20)
    ST_DATE = models.DateField()
    END_DATE = models.DateField()
    ST_TIME = models.TimeField()
    END_TIME = models.TimeField()
    Online_choises = (
        ('t', 'true'),
        ('f', 'false')
    )
    online = models.CharField(max_length=1)
    CAPACITY = models.IntegerField()
    PASSWORD = models.CharField(max_length=10)
    STATUS = models.CharField(max_length=20)
    image = models.ImageField(upload_to='events/',)
    
    # image = models.ImageField(upload_to='event_images/')
    # image = models.ImageField(upload_to='event_images/%Y/%m/%d/')
    # def image_url(self):
    #     if self.image:
    #         return reverse('event_image', args=[str(self.id)])
    #     else:
    #         return ''

    # locationـid = models.IntegerField()
    # TICKETS=models.ExpressionList([1])
    # GUESTS=models.ExpressionList([1])
    # FOLLOEWRS =models.ExpressionList([1])
    # LIKES =models.ExpressionList([1])
    # CREATED=models.ExpressionList([1])


    REQUIRED_FIELDS = ['ID','User_id','Title', 'organizer', 'Description', 'type', 'Category',
                       'sub_Category', 'venue_name', 'ST_DATE', 'END_DATE', 'ST_TIME', 'END_TIME', 'online',
                       'CAPACITY', 'PASSWORD', 'STATUS','image'
                       ]

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


