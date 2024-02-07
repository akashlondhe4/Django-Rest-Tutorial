from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    #  1. Function Based url
    path('list/', views.movie_list, name='watchlist'),
    path('list/<int:pk>', views.movie_detail, name='watchlist-detail'),
    path('stream/', views.stream_list, name='streamplatform-list'),
    path('stream/<int:pk>', views.stream_detail, name='streamplatform-detail'),

    # 2. class Based url
    path('classlist/', views.StreamPlatformList.as_view(), name='streamplatform-classlist'),
    path('classlist/<int:pk>', views.StreamPlatformDetails.as_view(), name='streamplatform-classdetails'),

    # 3. using mixing
    path('mxlist/', views.StreamingPlatformsList.as_view(), name='streamplatform-mixinglist'),
    path('mxlist/<int:pk>', views.StreamingPlatformsDetails.as_view(), name='streamplatform-mixingdetails'),

    # 4. Using generic class-based views
    path('gcbstream/', views.StreamingLists.as_view(), name='streamplatform-gcbstreamlist'),
    path('gcbstream/<int:pk>', views.StreamingDetails.as_view(), name='streamplatform-gcbstreamdetails'),

    # 5 using url for endpoint for the highlighted movie list and streaming platform list
    path('', views.api_root),

    #
    path('list/<int:pk>/review/', views.ReviewsListView.as_view(), name='reviews-list'),
    path('review/<int:pk>', views.ReviewsDetailsView.as_view(), name='review-details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)