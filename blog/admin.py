from django.contrib import admin

# Register your models here.
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    # ...
    search_fields = ["title"]
    list_display = ["title", "pub_date", "was_published_recently"]


class CommentAdmin(admin.ModelAdmin):
    # ...
    list_display = ["post", "author", "created_date"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
