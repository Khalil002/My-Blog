
import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class PostManager(models.Manager):
    """Default manager — transparently excludes soft-deleted posts."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField("date published")
    deleted = models.BooleanField(default=False)

    objects = PostManager()          # excludes deleted (default)
    all_objects = models.Manager()   # raw access when needed

    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.boolean = True
    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.short_description = "Published recently?"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return self.text