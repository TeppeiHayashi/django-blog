from django.shortcuts import  get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from blog.models import Post, Comment, Reply
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
 
    
    