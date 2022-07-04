from django.contrib import admin

from app import models


class VideoAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ['title', 'channel_title', 'published_at']
    list_filter = ['published_at']
    search_fields = ['title', 'description', 'channel_title']


admin.site.register(models.Video, VideoAdmin)
