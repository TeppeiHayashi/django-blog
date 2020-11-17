from django.db import models
from django.conf import settings
from django.utils import timezone
from markdownx.models import MarkdownxField  # @UnresolvedImport
from django.db.models.fields.related import ForeignKey
 
class Tag(models.Model):
    name = models.CharField('タグ名', max_length=50)
 
    def __str__(self):
        return self.name
 
class Post(models.Model):
    title = models.CharField('タイトル', max_length=80)
    author = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='投稿者')
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    description = MarkdownxField('説明文', blank=True, null=True, help_text='一覧ページで表示される投稿の説明文です。')
    content = MarkdownxField('本文', help_text='Markdown形式で記述。')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    published_at = models.DateTimeField('公開日', blank=True, null=True)
    relation_posts = models.ManyToManyField('self',blank=True, null=True, verbose_name='関連記事')
     
    def publish(self):
        self.published_at = timezone.now()
        self.save()
         
    def __str__(self):
        return self.title
 
    class Meta:
        ordering = ['-created_at']
      
         
class Comment(models.Model):
    name = models.CharField('名前', max_length=20)
    text = MarkdownxField('本文', help_text='Markdown形式で記述できます。')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='対象記事', related_name='comments')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    is_approve = models.BooleanField(default=False)
     
    def approve(self):
        self.is_approve = True
     
     
class Reply(models.Model):
    name = models.CharField('名前', max_length=20)
    text = MarkdownxField('本文', help_text='Markdown形式で記述できます。')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント', related_name='replies')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    is_approve = models.BooleanField(default=False)
     
    def approve(self):
        self.is_approve = True
         