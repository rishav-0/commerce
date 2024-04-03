from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class  Category(models.Model):
    name = models.CharField(max_length=100)
    def  __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField( max_length=50)
    description = models.TextField(max_length = 300)
    price = models.FloatField()
    imgUrl = models.URLField(null=True, blank=True)
    isActive = models.BooleanField(default= True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user",blank = True, null=True)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, null= True, blank=True,related_name = "category")
    watchlist = models.ManyToManyField(User,blank=True,related_name="watchlist")
    def   __str__(self):
         return self.title