from lib2to3.pgen2 import token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User

from user_app.api.serializers import RegistrationSerialer
# from user_app import models
# from rest_framework_simplejwt.tokens import RefreshToken


#DOES NOT WORK, OLD ACCESS TOKEN IS STILL VALID UNTIL IT EXPIRES
#revokes access by generating a new token without sending it to client       
# def revoke_access_token( username):
#     print(username)
#     account = User.objects.get(username=username)
#     refresh = RefreshToken.for_user(user=account)
#     print({'detail':'access revoked for '+ username,'undisclosed_token':{
#                                 'refresh': str(refresh),
#                                 'access': str(refresh.access_token),
#                             }})
    
    
#logout 
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    # print(request.user.get_username())
    # revoke_access_token(username=request.user.get_username())
    
    # return Response(status=status.HTTP_200_OK)

#User Registration
@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerialer(data=request.data)
        data = {}
        
        if serializer.is_valid():
            account =serializer.save() # needs to be overwritten in serializer(2 password needs to be checked b4 saving one, email needs to be checked if unique)
            data['response'] = "Registration successful"
            data['username'] = account.username
            
            #using Token 
            token = Token.objects.get(user=account).key
            data['token'] = token
            
            # #USING JWT
            # refresh = RefreshToken.for_user(user=account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }
        else:
            data = serializer.errors
            
        return Response(data )  #to the client excluding password as it is write only
 

        
    