from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils import timezone


class Comment(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_date']

    def disapprove(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text