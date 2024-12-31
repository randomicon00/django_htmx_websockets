from django.db import models
from .constants import (
    ROOM_NAME_MAX_LENGTH,
    ROOM_VERBOSE_NAME,
    ROOM_VERBOSE_NAME_PLURAL,
    ROOM_ORDERING,
    MESSAGE_ORDERING,
    MESSAGE_CONTENT_PREVIEW_LENGTH,
    MESSAGE_VERBOSE_NAME,
    MESSAGE_VERBOSE_NAME_PLURAL,
)


class Room(models.Model):
    name = models.CharField(max_length=ROOM_NAME_MAX_LENGTH)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = ROOM_VERBOSE_NAME
        verbose_name_plural = ROOM_VERBOSE_NAME_PLURAL
        ordering = ROOM_ORDERING

    def __str__(self):
        return self.name

    def __repr__(self):
        description_preview = (
            f"{self.description[:30]}..."
            if len(self.description) > 30
            else self.description
        )
        return f"<Room(name='{self.name}', description='{description_preview}')>"


class Message(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = MESSAGE_VERBOSE_NAME
        verbose_name_plural = MESSAGE_VERBOSE_NAME_PLURAL
        ordering = MESSAGE_ORDERING

    def __str__(self):
        content_preview = (
            f"{self.content[:MESSAGE_CONTENT_PREVIEW_LENGTH]}..."
            if len(self.content) > MESSAGE_CONTENT_PREVIEW_LENGTH
            else self.content
        )
        return f"Message in {self.room.name} at {self.timestamp}: {content_preview}"

    def __repr__(self):
        content_preview = (
            f"{self.content[:MESSAGE_CONTENT_PREVIEW_LENGTH]}..."
            if len(self.content) > MESSAGE_CONTENT_PREVIEW_LENGTH
            else self.content
        )
        return (
            f"<Message(room='{self.room.name}', timestamp='{self.timestamp}', "
            f"content_preview='{content_preview}')>"
        )
