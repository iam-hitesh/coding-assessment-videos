from django.urls import path

from app import views

urlpatterns = [
    path('videos', views.YoutubeVideosViewSet.as_view(), name='get_videos'),
]
