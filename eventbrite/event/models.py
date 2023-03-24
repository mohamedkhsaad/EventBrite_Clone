from django.db import models
from eventbrite.settings import*
# Create your models here.

class event(models.Model):
    ID = models.IntegerField(unique=True)
    User_id=models.IntegerField(blank=False)
    Title=models.CharField(max_length=50)
    organizer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    organizer=models.CharField(max_length=50)
    Description=models.CharField(max_length=500)
    type=models.CharField(max_length=20)
    Category=models.CharField(max_length=10)
    sub_Category=models.CharField(max_length=10)
    venue_name=models.CharField(max_length=20)
    CATEGORY_ID=models.IntegerField()
    SUB_CATEGORY_ID =models.IntegerField()
    ST_DATE=models.DateField()
    END_DATE=models.DateField()
    ST_TIME =models.TimeField()
    END_TIME =models.TimeField()

    #ONLINE=models.BooleanField(default=False)
    Online_choises= (
        ('t', 'true'),
        ('f', 'false')
    )
    online = models.CharField(max_length=1)
    CAPACITY=models.IntegerField()
    PASSWORD =models.CharField(max_length=10)
    # EVENT_PHOTO=models.ImageField()
    locationـid=models.IntegerField()
    # TICKETS=models.ExpressionList([1])
    # GUESTS=models.ExpressionList([1])
    # FOLLOEWRS =models.ExpressionList([1])
    # LIKES =models.ExpressionList([1])
    # CREATED=models.ExpressionList([1])
    STATUS =models.CharField(max_length=20)
    REQUIRED_FIELDS =['ID', 'Title', 'organizer', 'Description', 'type', 'Category',
                       'sub_Category','venue_name','ST_DATE','END_DATE','ST_TIME','END_TIME','online',
                       'CAPACITY','PASSWORD','STATUS',
                       ]

    # TAGS =models.ExpressionList()




class category(models.Model):
    ID=models.IntegerField()
    Name=models.CharField(max_length=20)
    EVENT_ID=models.IntegerField()
    SUB_CATEGORY_ID=models.IntegerField()

    # CONSTRAINT [FK_CATEGORY.SUB_CATEGORY_ID]
    #     FOREIGN KEY ([SUB_CATEGORY_ID])
    #     REFERENCES [CATEGORY]([SUB_CATEGORY_ID])
class sub_category(models.Model):
    ID=models.IntegerField()
    EVENT_ID=models.IntegerField()
    NAME=models.CharField(max_length=20)

class Locations(models.Model):
    ID=models.IntegerField()
    EVENT_ID=list()
    USER_ID=list()
    adress=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    latitude=models.CharField(max_length=20)
    longitude=models.CharField(max_length=20)



# class Interests(models.Model):
#   ID=models.IntegerField()
#   TYPE=models.CharField(max_length=20)
#   Name=models.CharField(max_length=20)
#   user_id=models.IntegerField()
#   sub_category_id=models.IntegerField()

