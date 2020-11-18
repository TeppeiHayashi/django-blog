from django.shortcuts import render
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
            queryset = queryset.filter(tags=tag)
            
        return queryset