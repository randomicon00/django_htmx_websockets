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
    """
    Generates a unique slug for the given model instance based on its name.
    If a slug already exists, it appends a counter until a unique slug is found.
    """
    base = slugify(instance.name.strip())
    slug = base
    qs = instance.__class__.objects.filter(slug=slug)
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    counter = 1
    while qs.exists():
        slug = f"{base}-{counter}"
        qs = instance.__class__.objects.filter(slug=slug)
        if instance.pk:
            qs = qs.exclude(pk=instance.pk)
        counter += 1
    return slug


class Room(models.Model):
    """Model representing a chat room."""

    name = models.CharField(
        max_length=ROOM_NAME_MAX_LENGTH,
        verbose_name="Room Name",
        help_text="Enter room's name.",
        unique=True,
    )
    slug = models.SlugField(
        max_length=ROOM_NAME_MAX_LENGTH,
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
        if not self.slug or getattr(self, "_original_name", None) != self.name:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)
        self._original_name = self.name

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
        null=True,  # column can be NULL in database
        blank=True,  # field can be blank in fields
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
        indexes = [models.Index(fields=["-timestamp"], name="timestamp_desc_idx")]

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
