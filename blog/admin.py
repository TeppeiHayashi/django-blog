from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Tag, Comment, Reply
# Register your models here.

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Tag)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Reply, MarkdownxModelAdmin)
