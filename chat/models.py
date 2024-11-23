from django.db import models


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.content)[:50]}..."  # Short preview of the message


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
