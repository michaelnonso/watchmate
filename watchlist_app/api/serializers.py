from asyncore import read
from dataclasses import fields
from importlib.abc import ExecutionLoader
from multiprocessing.sharedctypes import Value
from platform import platform
from pyexpat import model
from django.forms import ValidationError
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

#using validators----validator function
# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too short!")
#     return value
  
class ReviewSerializer(serializers.ModelSerializer):
    user_reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model= Review
        # fields = "__all__"
        exclude = ("watchlist",)
        
        
        
class WatchListSerializer(serializers.ModelSerializer):
    #variable name must be mapped to related field in models
    #reviews = ReviewSerializer(many=True, read_only=True)  #readonly use dont need to pass it when doing POST.
    platform = serializers.CharField(source='platform.name')
    length_title= serializers.SerializerMethodField()  # Custom Field
    class Meta:
        model = WatchList 
        fields = "__all__"
        # exclude= ["active"]
        # fields = ["id", "name", "description"]
    
        
    def get_length_title(self,object):  #Function calculating the custom  field
        return len(object.title)
 
class StreamPlatformSerializer(serializers.ModelSerializer):
    #this is the case of a nested serializer
    # watchlistserializer is used inside StreamPlatformSerializer
    #custom field is created that mirrors the relationship in reverse
    watchlist = WatchListSerializer(many=True, read_only=True)  #readonly use dont need to pass it when doing POST.
    #watchlist = serializers.StringRelatedField(many=True) #using serialiser relationship
    #watchlist = serializers.PrimaryKeyRelatedField(many=True,read_only=True ) #using serialiser relationship
    #watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watch-detail'
    # )
    class Meta:
        model = StreamPlatform
        fields ="__all__"
        
  
#MODEL SERIALIZER CODE  
# class MovieSerializer(serializers.ModelSerializer):
#     length_name= serializers.SerializerMethodField()  # Custom Field
#     class Meta:
#         model = Movie
#         fields = "__all__"
#         # exclude= ["active"]
#         # fields = ["id", "name", "description"]
    
        
#     def get_length_name(self,object):  #Function calculating the custom  field
#         return len(object.name)
        
    # #Validator methods
    # #Object level validation   
    # def validate(self, data): 
    #     if data['name']== data['description']: 
    #         raise serializers.ValidationError("Name and description should be diffrent")
    #     else:
    #         return data
    
    # # field level validation
    # def validate_name(self, value): #should be named with the validated field after the _
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short!")
    #     return value
        
    
        


#USING SERIALIZERS
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])      # using validators
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#     # we can add methods to validate,create,update and other crud activities 


#     def create(self, validated_data):   #when posting
#         return Movie.objects.create(**validated_data)


#     #PUT:::complete update
#     def update(self,instance,validated_data):  #instance is the old value
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     #Validator methods
    
#     #Object level validation   
#     def validate(self, data): 
#         if data['name']== data['description']: 
#             raise serializers.ValidationError("Name and description should be diffrent")
#         else:
#             return data
    
#     # # field level validation
#     # def validate_name(self, value): #should be named with the validated field after the _
#     #     if len(value)<2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     return value
        
    
        