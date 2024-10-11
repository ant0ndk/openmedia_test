from django.db import models
from django.utils import timezone


class Page(models.Model):
    url = models.URLField(max_length=500)
    h1_count = models.IntegerField(default=0)
    h2_count = models.IntegerField(default=0)
    h3_count = models.IntegerField(default=0)
    links = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
