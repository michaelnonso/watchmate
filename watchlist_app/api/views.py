from multiprocessing import managers
from platform import platform
from tkinter import N, W
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle, ScopedRateThrottle
# from rest_framework import mixins

from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCPagination
from watchlist_app.api.throttle import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.permissions import IsAdminOrReadOnly,IsUserReviewerOrAdminOrReadOnly
from watchlist_app.models import (WatchList
                                  , StreamPlatform, Review)
from watchlist_app.api.serializers import (WatchListSerializer
                                           , StreamPlatformSerializer
                                           , ReviewSerializer)

# Create your views here.


#CLASS BASED VIEWS =================================

#USING GENERIC VIEW CLASSES ALONE
class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class =ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        pk= self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
       
        
        #to make sure same user does not submit multiple reviews for one movie
        
        user_reviewer = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,user_reviewer=user_reviewer)
        
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating'] 
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2 
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, user_reviewer=user_reviewer) 
        
        

class ReviewList(generics.ListAPIView): #give me all reviews for watchlist with a particular id
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # ADDING OBJECT LEVEL PERMISSINS
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]  
    filterset_fields = ['user_reviewer__username', 'active'] #review_user is the property defined in user which carries retalionship to User model
                                                            #__username is the property to be retrieved from the User model
    #overwriting the queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsUserReviewerOrAdminOrReadOnly]
    #throttle_classes =[UserRateThrottle, AnonRateThrottle]
    throttle_classes =[ScopedRateThrottle]
    throttle_scope = 'review-detail'



#using mixins we write methods such as get and post
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)



#GenericAPIView watchlist for test search test purposes
class WatchListG(generics.ListAPIView):
    queryset = WatchList.objects.all() #queryset object
    serializer_class = WatchListSerializer
    pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    #pagination_class = WatchListCPagination
     
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title','platform__name']
    
    
    #ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    
 

class WatchListAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movie = WatchList.objects.all() #queryset object
        serializer = WatchListSerializer(movie, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
                
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
            
    def put(self, request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer= WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# USING MODELVIEWSET
class StreamPlatforms(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
    
    
    
    
    
            
 # USING VIEWSETS  
# class StreamPlatforms(viewsets.ViewSet):
#     def list(self,request): 
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self,request,pk=None): 
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
    
# class StreamingPlatformListAv(APIView):
#     def get(self,request): 
#         platform = StreamPlatform.objects.all() #queryset object
#         serializer = StreamPlatformSerializer(platform, many=True )
#         #serializer = StreamPlatformSerializer(platform, many=True , context={'request': request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
                
# class StreamingPlatformDetailAV(APIView):
#     def get(self,request,pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(platform)
#         #serializer = StreamPlatformSerializer(platform, context={'request': request})
#         return Response(serializer.data)
            
#     def put(self, request,pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer= StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk):
#         movie = StreamPlatform.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)    
        
        











#METHOD BASED VIEWS =================================
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movie = Movie.objects.all() #queryset object
#         serializer = MovieSerializer(movie, many=True)
#         print(serializer.data)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# #@api_view()  #get by default
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request,pk):
#     if request.method=='GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method=='PUT': #update every field
#         movie = Movie.objects.get(pk=pk)
#         serializer= MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method=='DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

 