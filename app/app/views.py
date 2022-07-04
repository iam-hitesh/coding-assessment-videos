from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.pagination import CursorPagination

from app import models
from app import serializers


class ResultsPagination(CursorPagination):
    page_size = 25
    page_size_query_param = 'size'
    max_page_size = 100


class YoutubeVideosViewSet(generics.ListAPIView):
    search_fields = ['title', 'description']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ['channel_id', 'channel_title']
    ordering = ['-published_at', ]
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoSerializer
    pagination_class = ResultsPagination
