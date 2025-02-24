from django.db import models
from django.utils.text import slugify, Truncator

from .constants import (
    ROOM_NAME_MAX_LENGTH,
    ROOM_VERBOSE_NAME,
    ROOM_VERBOSE_NAME_PLURAL,
    ROOM_ORDERING,
    MESSAGE_ORDERING,
    MESSAGE_CONTENT_PREVIEW_LENGTH,
    MESSAGE_VERBOSE_NAME,
    MESSAGE_VERBOSE_NAME_PLURAL,
    ROOM_DESCRIPTION_PREVIEW_LENGTH,
)


def generate_unique_slug(instance):
    base_slug = slugify(instance.name.strip())
    slug = base_slug
    counter = 1
    while instance.__class__.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class Room(models.Model):
    """Model representing a chat room."""

    name = models.CharField(
        max_length=ROOM_NAME_MAX_LENGTH,
        verbose_name="Room Name",
        help_text="Enter the name of the room.",
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Unique slug for the room.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Provide a brief description of the room (optional).",
    )

    class Meta:
        verbose_name = ROOM_VERBOSE_NAME
        verbose_name_plural = ROOM_VERBOSE_NAME_PLURAL
        ordering = ROOM_ORDERING

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if not provided
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Room(name='{self.name}', slug='{self.slug}', description_preview='{self._get_description_preview()}')>"

    def _get_description_preview(self):
        """Helper method to preview the description."""
        return Truncator(self.description).chars(
            ROOM_DESCRIPTION_PREVIEW_LENGTH, truncate="..."
        )


class Message(models.Model):
    """Model representing a message within a chat room."""

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Room",
        help_text="Select the room this message belongs to.",
    )
    content = models.TextField(
        verbose_name="Message Content",
        help_text="Enter the content of the message.",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Timestamp",
        help_text="The time this message was created.",
    )

    class Meta:
        verbose_name = MESSAGE_VERBOSE_NAME
        verbose_name_plural = MESSAGE_VERBOSE_NAME_PLURAL
        ordering = MESSAGE_ORDERING

    def __str__(self):
        return f"Message in {self.room.name} at {self.timestamp}: {self._get_content_preview()}"

    def __repr__(self):
        return (
            f"<Message(room='{self.room.name}', timestamp='{self.timestamp}', "
            f"content_preview='{self._get_content_preview()}')>"
        )

    def _get_content_preview(self):
        """Helper method to preview the content."""
        return Truncator(self.content).chars(
            MESSAGE_CONTENT_PREVIEW_LENGTH, truncate="..."
        )
