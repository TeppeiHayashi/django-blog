from django.shortcuts import  get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Q, Count
from blog.models import Post, Comment, Reply, Tag
from blog.forms import CreateCommentForm, CreateReplyForm
# Create your views here.


class IndexView(generic.ListView):
    '''
        Post一覧ページ
    '''
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    base_queryset = None
    
    def get_queryset(self):
        '''
           Postのqueryset下記の条件により絞り込む。
           ・ アクセスが管理者かどうか
           ・ キーワード検索か
        '''
        
        if not self.request.user.is_superuser:
            self.base_queryset = self.model.objects.published()
        else:
            self.base_queryset = super().get_queryset()
        
        queryset = self.base_queryset

        # キーワード検索
        keyword = self.request.GET.get('keyword', None)
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | 
                                       Q(description__icontains=keyword) | 
                                       Q(content__icontains=keyword))
            
        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post_pk_list = self.base_queryset.values_list('pk', flat=True)
        ctx['tags'] = Tag.objects.filter(post__in=post_pk_list).annotate(Count('post'))
        return ctx
    
class PostDetailView(generic.DetailView):
    '''
        Post詳細ページ
    '''
    model = Post
    
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if (not self.request.user.is_superuser) and (not post.published_at):
            '''
                 >>> 404 'superuserではない場合 かつ 公開されていない投稿の場合'
            '''
            raise Http404()
        
        return post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CreateCommentForm()
        ctx['reply_form'] = CreateReplyForm()
        ctx['breadcrumb'] = [
                {'name' : self.object.tags.all()[0].name, 'link' : reverse_lazy('blog:tag_post_list', kwargs=dict(name=self.object.tags.all()[0].name))},
                {'name' : self.object.title, 'link' :None }
            ]
        return ctx
        
class CreateComment(generic.CreateView):
    '''
        CreateCommentFormのPOST送信後の処理。
    '''
    http_method_names = ['post'] # only request.POST 
    model = Comment
    form_class = CreateCommentForm
    
    def get_form_kwargs(self):
        '''
            Commentに紐づくPostを取得、追加。
        '''
        kwargs = super().get_form_kwargs()
        kwargs['post'] = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return kwargs
    
    def form_valid(self, form):
        form.instance.is_approve = self.request.user.is_superuser
        messages.success(self.request, 'コメントを送信しました。管理者が承認することでページに表示されます。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'コメントの投稿に失敗しました。内容を確認してください。')
        return super().form_invalid(form)
        
        
class CreateReply(generic.CreateView):
    '''
        ReplyCommentFormのPOST送信後の処理。        
    '''
    http_mehod_names = ['post'] # only request.POST 
    model = Reply
    form_class = CreateReplyForm
    
    def get_form_kwargs(self):
        '''
            Replyに紐づくCommentを取得、追加。
        '''
        kwargs = super().get_form_kwargs()
        kwargs['comment'] = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        return kwargs
    
    def form_valid(self, form):
        form.instance.is_approve = self.request.user.is_superuser
        messages.success(self.request, 'コメントを送信しました。 管理者が承認することでページに表示されます。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'コメントの投稿に失敗しました。内容を確認してください。')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs = {'pk' : Comment.objects.get(pk = self.kwargs.get('pk')).post.pk})
 
 
class TagPostListView(IndexView):
    '''
        タグでの絞り込み検索
        blog.views.IndexViewを継承している。
    '''
    model = Post
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_name = self.kwargs.get('name', None)
        
        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)
            return queryset
        
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['breadcrumb'] = [
                {'name' : self.kwargs.get('name'), 'link' :None }
            ]
        
        return ctx;
    