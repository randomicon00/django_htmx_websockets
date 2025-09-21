# Generated manually for read status feature

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_at',
            field=models.DateTimeField(
                blank=True,
                help_text='The time this message was read by the recipient.',
                null=True,
                verbose_name='Read At'
            ),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['read_at'], name='read_at_idx'),
        ),
    ]
