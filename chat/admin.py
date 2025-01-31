from django.contrib import admin
from .models import Message, Room


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("content", "timestamp")
    search_fields = ("content",)
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    list_filter = ("name",)
    ordering = ("name",)
