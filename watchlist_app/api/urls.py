
import re
from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from watchlist_app.api.views import movie_list, movie_detail
from watchlist_app.api.views import (WatchDetailAV, WatchListAv
                                     ,StreamPlatforms
                                     , ReviewList, ReviewDetail,ReviewCreate, WatchListG)
from watchlist_app.models import StreamPlatform

router = DefaultRouter()
router.register('streamplatforms',StreamPlatforms,basename='streamplatforms')

urlpatterns = [
    #path('watchlist/',WatchListAv.as_view(), name='watch-list'),
    path('watchlist/',WatchListG.as_view(), name='watch-listG'),
    path('watchlist/<int:pk>/',WatchDetailAV.as_view(), name='watch-detail'),
    
    path('', include(router.urls)),
    
    # path('streamplatforms/',StreamingPlatformListAv.as_view(), name='streamplatforms-list'),
    # path('streamplatforms/<int:pk>/',StreamingPlatformDetailAV.as_view(), name='streamplatforms-detail'),
   
    path('watch/<int:pk>/review-create/',ReviewCreate.as_view(), name='review-create'), #end point is called when review needs to be created on a particular movie
    path('watch/<int:pk>/review/',ReviewList.as_view(), name='review-list'),    # end point is called for all the reviews a particular movie has
    path('watch/review/<int:pk>/',ReviewDetail.as_view(), name='review-detail'),  #end point is called when a review on a movie needs to be read or opened


    # path('review/',ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(), name='review-detail'),

]


# urlpatterns = [
#     path('list/',movie_list, name='movie-list'),
#     path('<int:pk>',movie_detail, name='movie-detail'),
# ]
