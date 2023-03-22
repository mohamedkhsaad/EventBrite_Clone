from django.db import models

# Create your models here.

class event(models.Model):
    ID = models.IntegerField()
    User_id=models.IntegerField()
    Title=models.CharField(max_length=50)
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
    ONLINE=models.BooleanField()
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
    # TAGS =models.ExpressionList()
# class user(models.Model):
#     ID=models.IntegerField()
#     F_NAME=models.CharField(max_length=20)
#     L_NAME=models.CharField(max_length=20)
#     EMAIL=models.EmailField()
#     PASSWORD=models.CharField(max_length=20)

#     GENDER =models.Choices("male","female")
#     AGE =models.IntegerField()
#     BIRTH_DATE=models.DateField()
#     PHONE =models.CharField(max_length=20)

#     CITY=models.CharField(max_length=20)
#     COUNTRY=models.CharField(max_length=20)
#     ADDRESS =models.CharField(max_length=20)
#     LOCATION_ID =models.IntegerField()

#     DISCOUNT_ID=models.IntegerField()
                              
#     INTERESTS_ID=list()
#     EVENT_CREATED=list()
#     TICKETS_ID=list()
#     FOLLOWERS=list()


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

