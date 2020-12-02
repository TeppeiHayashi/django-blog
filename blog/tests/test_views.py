'''
    Viewに関するテストモジュール
'''


from django.urls import resolve, reverse
from django.test import TestCase, Client
from blog import views
from blog.models import Post, Tag
from blog.factories import UserFactory, PostFactory, TagFactory
from blog.forms import CreateCommentForm,CreateReplyForm
    
class IndexPageTest(TestCase):
    
    def setUp(self):
        self.superuser = UserFactory(is_staff=True, is_superuser=True)
        self.nomaluser = UserFactory()
    
    def test_root_url_resolve_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, views.IndexView)
        
        
    def test_the_number_of_posts_to_display_when_a_user_visits(self):
        '''
            superuserのリクエストはすべての投稿を表示
            それ以外のユーザーは公開済みの投稿を表示
        '''
        self.assertEqual(Post.objects.all().count(), 0)
        non_published_count = 2
        published_count = 3
        PostFactory.create_batch(size=non_published_count,
                                 author=self.superuser,
                                 published_at=None)
        PostFactory.create_batch(size=published_count,
                                 author=self.superuser)
        
        
        # superuserのリクエスト
        client = Client()
        client.force_login(self.superuser)
        response = client.get('/')
        
        self.assertTrue(response.wsgi_request.user.is_superuser)        
        self.assertEqual(len(response.context['posts']), non_published_count + published_count)
        self.assertQuerysetEqual(response.context['posts'], Post.objects.all(), transform= lambda x:x)
        
        
        # 一般ユーザーのリクエスト
        response = self.client.get('/')
        self.assertIn('posts', response.context)
        self.assertTrue(Post.objects.all().count() == non_published_count + published_count)
        self.assertTrue(len(response.context['posts']) == published_count)
        self.assertQuerysetEqual(response.context['posts'], Post.objects.published(), transform=lambda x: x) 

      
    def test_get_posts_by_filtering_tag(self):
        '''
            query_stringにTagが指定された際は、そのTagと紐づいたPostのみ取得する。
        '''
        
        tags = []
        tag_names = ['Python', 'Django', 'Kaggle']
        for tag_name in tag_names:
            tags.append(TagFactory(name=tag_name))
        # > [<Tag: Python>, <Tag: Django>, <Tag: Kaggle>]
        
        self.assertEquals(Tag.objects.all().count(), len(tags))
                
        PostFactory(author=self.superuser, tags=(tags[0],))
        PostFactory(author=self.superuser, tags=(tags[0], tags[2]))
        PostFactory(author=self.superuser, tags=(tags[1], tags[2]))
            
        self.assertEquals(Post.objects.all().count(), 3)
        
        client = Client()
        client.force_login(self.superuser)
        response = client.get('/?tag=1')
        
        tag_pk = response.wsgi_request.GET.get('tag', None)
        self.assertEquals(tag_pk , '1')
        
        tag = Tag.objects.get(pk=tag_pk)
        self.assertEquals(tag.name, 'Python') # pkは１から
        self.assertEquals(Post.objects.filter(tags=int(tag_pk)).count(), 2)
        self.assertEquals(response.context['posts'].count(), 2)
    
    def test_pagination(self):
        '''
            ページネーションの動作確認
        '''
        
        # 1ページ当たりの表示するPost数
        views.IndexView.paginate_by = 10
        
        # 15件のPostを作成
        PostFactory.create_batch(size=15, author = self.superuser)
        
        # 1ページ目
        response = self.client.get('/')
        self.assertIn('paginator', response.context)
        self.assertEquals(10, response.context['posts'].count())
        self.assertEquals(15, Post.objects.all().count())
        
        # 2ページ目
        response = self.client.get('/?page=2')
        self.assertEquals(5, response.context['posts'].count())
        
        # 3ページ目
        response = self.client.get('/?page=3')
        self.assertEquals(404, response.status_code)
 
 
   
class PostDetailPageTest(TestCase):
    '''
        Detailページのテストクラス reverse('blog:post_detail', pk=Post.ok) 
    '''
    
    def setUp(self):
        self.superuser = UserFactory(is_staff=True, is_superuser=True)
        self.nomaluser = UserFactory()
        
        self.published_post = PostFactory() # pk = 1
        self.non_published_post = PostFactory(published_at=None) # pk = 2    
    
    def test_detail_url_resolve_to_detail_page_view(self):
        found = resolve('/detail/1')
        self.assertEqual(found.func.view_class, views.PostDetailView)

    def test_get_the_specified_id_post(self):
        '''
            detail/<int:pk>のリクエストされたとき
        '''
        response = self.client.get('/detail/1')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertTrue(response.context['post'].published_at)
        self.assertEqual(self.published_post, response.context['post'])
        
    def test_when_a_non_published_post_id_is_specified_in_the_request(self):
        '''
            非公開のPost IDを指定されたとき
            ・superuser > 表示
            ・non_superuser > 非表示
        '''
        path = '/detail/2'
        
        client = Client()
        client.force_login(self.superuser)
        response = client.get(path)
        self.assertFalse(response.context['post'].published_at)
        self.assertEqual(self.non_published_post, response.context['post'])
        
        
        response = self.client.get(path)
        self.assertEqual(404, response.status_code)
        
        
      
    def test_when_a_non_existent_post_id_is_specified_in_the_request(self):
        '''
            存在しないPost IDを指定されたとき
        '''
        response = self.client.get('/detail/3')
        self.assertEqual(404, response.status_code)
        
      
    def test_comment_and_reply_form(self):
        '''
            コメントフォームがコンテキストに含まれているか
        '''
        
        response = self.client.get('/detail/1')
        self.assertIn('comment_form', response.context)
        self.assertIn('reply_form', response.context)
        self.assertTrue(isinstance(response.context['comment_form'], CreateCommentForm))
        self.assertTrue(isinstance(response.context['reply_form'], CreateReplyForm))
        
    def test_create_comment(self):
        '''
            コメント作成のテスト
        '''
        
        form = CreateCommentForm({
                'name' : '名無し',
                'text' :'コメントのテストです。'
            }, post=self.published_post)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, '名無し')
        self.assertEqual(comment.text, 'コメントのテストです。')
        self.assertEqual(comment.post, self.published_post)
        
                