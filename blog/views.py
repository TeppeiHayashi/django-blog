from django.shortcuts import render
from django.http import Http404
from django.views import generic
from blog.models import Post
# Create your views here.


class IndexView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    base_queryset = None
    
    def get_queryset(self):
        
        if not self.request.user.is_superuser:
            self.base_queryset = self.model.objects.published()
        else:
            self.base_queryset = super().get_queryset()
        
        queryset = self.base_queryset
        tag = self.request.GET.get('tag', None)
        
        if tag:
            queryset = queryset.filter(tags=int(tag))
            
        return queryset
    
    
class PostDetailView(generic.DetailView):
    model = Post
    
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if (not self.request.user.is_superuser) and (not post.published_at):
            '''
                 >>> 404 'superuserではない場合 かつ 公開されていない投稿の場合'
            '''
            raise Http404()
        
        return post

