from rest_framework import serializers
from app import models


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        exclude = ['id']
