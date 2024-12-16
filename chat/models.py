from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["name"]  # Optional: Orders rooms alphabetically

    def __str__(self):
        return f"Room: {self.name}"

    def __repr__(self):
        return f"<Room(name={self.name}, description={self.description})>"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-timestamp"]  # Orders messages by most recent first

    def __str__(self):
        preview = f"{self.content[:50]}..." if len(self.content) > 50 else self.content
        return f"Message at {self.timestamp}: {preview}"

    def __repr__(self):
        return f"<Message(room={self.room.name}, timestamp={self.timestamp}, content_preview='{self.content[:50]}')>"
