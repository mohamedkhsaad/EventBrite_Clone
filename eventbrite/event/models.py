from django.db import models
from eventbrite.settings import *
from user.models import *




# class Interests(models.Model):
#     category_name = models.CharField(max_length=255)
#     user_id = models.IntegerField(unique=False)

# class UserInterest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     interest = models.ForeignKey(Interests, on_delete=models.CASCADE)

#    def __str__(self):
#         return f"{self.user.email} - {self.interest.category_name}" 


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    category_name = models.CharField(max_length=255)

  
    def __str__(self):
        return f"{self.user.email} - {self.interest.category_name}" 
  

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
    Description = models.CharField(max_length=500)
    type = models.CharField(max_length=20)
    category_name = models.CharField(max_length=10)
    sub_Category = models.CharField(max_length=10)
    venue_name = models.CharField(max_length=20)
    CATEGORY_ID = models.IntegerField()
    SUB_CATEGORY_ID = models.IntegerField()
    ST_DATE = models.DateField()
    END_DATE = models.DateField()
    ST_TIME = models.TimeField()

    END_TIME = models.TimeField()

    # ONLINE=models.BooleanField(default=False)
    Online_choises = (
        ('t', 'true'),
        ('f', 'false')
    )
    online = models.CharField(max_length=1)
    CAPACITY = models.IntegerField()
    PASSWORD = models.CharField(max_length=10)
    # EVENT_PHOTO=models.ImageField()
    locationـid = models.IntegerField()
    # TICKETS=models.ExpressionList([1])
    # GUESTS=models.ExpressionList([1])
    # FOLLOEWRS =models.ExpressionList([1])
    # LIKES =models.ExpressionList([1])
    # CREATED=models.ExpressionList([1])
    STATUS = models.CharField(max_length=20)
    REQUIRED_FIELDS = ['ID', 'Title', 'organizer', 'Description', 'type', 'Category',
                       'sub_Category', 'venue_name', 'ST_DATE', 'END_DATE', 'ST_TIME', 'END_TIME', 'online',
                       'CAPACITY', 'PASSWORD', 'STATUS',
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


