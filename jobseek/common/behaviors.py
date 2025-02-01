import django.utils.timezone
from django.db import models


class Timestampable(models.Model):
    created_at = models.DateTimeField(default=django.utils.timezone.now, help_text='created date')
    modified_at = models.DateTimeField(auto_now=True, help_text='modified date')

    class Meta:
        abstract = True
