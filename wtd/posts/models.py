from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils import timezone


class PostQuerySet(models.query.QuerySet):

    def posts(self, user):
        return self.filter(author=user)

    def get_post_count(self, user):
        return self.filter(author=user).count()


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    cover = models.ImageField(upload_to='images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class LikesQuerySet(models.query.QuerySet):

    def does_user_like(self, user):

        return self.filter(user=user)

    def get_num_likes(self, post):
        return self.filter(post=post).count()

    def get_likes(self, post):
        return self.filter(post=post)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='user')
    created = models.DateTimeField(auto_now_add=True)
    objects = LikesQuerySet.as_manager()

