from msilib.schema import Class
from wsgiref.validate import validator
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE,related_name="watchlist")  #related name is used for reverse I.e given the platform you can get the watchlists
    active= models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)  #time frame is stored as soon as odject is cfreated 
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    user_reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True) #at time of creation
    update = models.DateTimeField(auto_now=True) #at time of update
    active = models.BooleanField(default=True)  
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE,related_name="reviews")
    
    def __str__(self):
         return str(self.rating)+ "|" + self.watchlist.title

#OLD MODEL
# class Movie(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     active= models.BooleanField(default=True)

#     def __str__(self):
#         return self.name