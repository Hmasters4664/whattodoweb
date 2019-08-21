from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils import timezone


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class BlogQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status=1)

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status=0)


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    objects = BlogQuerySet.as_manager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class BlogCommentQuerySet(models.query.QuerySet):

    def get_comments(self, post):

        return self.filter(post=post)


class BlogComment(models.Model):
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=True)
    objects = BlogCommentQuerySet.as_manager()

    class Meta:
        ordering = ['-created_date']

    def disapprove(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text




