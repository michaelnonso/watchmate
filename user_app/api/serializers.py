from dataclasses import fields
import email
from re import U
from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerialer(serializers.ModelSerializer): 
    #an extra field is defined for confirmation
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True) 
    
    class Meta:
        model = User
        fields  = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }       
        #by default django doesnt support unique email addresses        

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be the same'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account
        
            
            