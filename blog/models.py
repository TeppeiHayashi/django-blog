from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField  # @UnresolvedImport
from django.db.models.fields.related import ForeignKey

class Tag(models.Model):
    name = models.CharField('タグ名', max_length=50, unique=True, null=False)
  
    def __str__(self):
        return self.name

class PostQuerySet(models.QuerySet):
    
    def published(self):
        '''公開済みの記事を取得'''
        return self.filter(published_at__lte=timezone.now())
        
  
class Post(models.Model):
    title = models.CharField('タイトル', max_length=80)
    author = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='投稿者')
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='タグ')
    description = MarkdownxField('説明文', blank=True, null=True, help_text='一覧ページで表示される投稿の説明文です。')
    content = MarkdownxField('本文', help_text='Markdown形式で記述。')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    published_at = models.DateTimeField('公開日', blank=True, null=True)
    relation_posts = models.ManyToManyField('self',blank=True, null=True, verbose_name='関連記事')
      
    objects = PostQuerySet.as_manager()
      
    def publish(self):
        self.published_at = timezone.now()
        self.save()
          
    def __str__(self):
        return self.title
  
    class Meta:
        ordering = ['-created_at']
       
 
class CommentReplyQueryset(models.QuerySet):
    
    def approved(self):
        self.filter(is_approve=True) 
          
class Comment(models.Model):
    name = models.CharField('名前', max_length=20)
    text = MarkdownxField('本文', help_text='Markdown形式で記述できます。')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='対象記事', related_name='comments')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    is_approve = models.BooleanField(default=False)
    
    objects = CommentReplyQueryset.as_manager()
    
    def approve(self):
        self.is_approve = True
      
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk' : self.post.pk})  
    
class Reply(models.Model):
    name = models.CharField('名前', max_length=20)
    text = MarkdownxField('本文', help_text='Markdown形式で記述できます。')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント', related_name='replies')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    is_approve = models.BooleanField(default=False)
    
    objects = CommentReplyQueryset.as_manager()
    
    def approve(self):
        self.is_approve = True
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk' : self.comment.post.pk})