from django.contrib import admin
from .models import Message, Room

"""Admin configurations for the chat application models."""


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = "timestamp"
    list_display = ("id", "content", "room", "timestamp")
    search_fields = ("content", "room__name")
    list_filter = ("room",)
    ordering = ("-timestamp",)
    list_select_related = ("room",)
    list_per_page = 50
    autocomplete_fields = ("room",)
    readonly_fields = ("timestamp",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    list_filter = ("name",)
    ordering = ("name",)
    list_per_page = 50
