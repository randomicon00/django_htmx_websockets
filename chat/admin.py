from django.contrib import admin
from .models import Message, Room


class MessageAdmin(admin.ModelAdmin):
    list_display = ("content", "timestamp")
    search_fields = ("content",)
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)

class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


admin.site.register(Message, MessageAdmin)
admin.site.register(Room, RoomAdmin)
