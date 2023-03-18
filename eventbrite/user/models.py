from django.db import models

# Create your models here.
class user(models.Model):
    ID=models.IntegerField()
    F_NAME=models.CharField(max_length=20)
    L_NAME=models.CharField(max_length=20)
    EMAIL=models.EmailField()
    PASSWORD=models.CharField(max_length=20)

    GENDER =models.Choices("male","female")
    AGE =models.IntegerField()
    BIRTH_DATE=models.DateField()
    PHONE =models.CharField(max_length=20)

    CITY=models.CharField(max_length=20)
    COUNTRY=models.CharField(max_length=20)
    ADDRESS =models.CharField(max_length=20)
    LOCATION_ID =models.IntegerField()

    DISCOUNT_ID=models.IntegerField()
                              
    INTERESTS_ID=list()
    EVENT_CREATED=list()
    TICKETS_ID=list()
    FOLLOWERS=list()
    
class Interests(models.Model):
  ID=models.IntegerField()
  TYPE=models.CharField(max_length=20)
  Name=models.CharField(max_length=20)
  user_id=models.IntegerField()
  sub_category_id=models.IntegerField()