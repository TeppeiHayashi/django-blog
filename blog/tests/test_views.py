from django.urls import resolve
from django.test import TestCase, Client
from blog import views
from blog.models import Post, Tag
from blog.tests.testcases import SuperUserTestCase

    
class IndexPageTest(SuperUserTestCase):
    
    def test_root_url_resolve_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, views.IndexView)
        
    def test_when_visited_by_non_superuser(self):
        '''
        ToDo:
            ・superuser以外のuserが訪れたとき
            ・viewに渡すcontextには公開済みのPostのみ格納されている。
        '''
        self.assertEqual(Post.objects.all().count(), 0)
        
        post_count = 5
        published_count = post_count - 2
        for i in range(post_count):
            post = create_post()
            post.title += f' {str(i)}'
            post.author = self.user
            if i < published_count: post.publish()
            post.save()
        
        response = self.client.get('/')
        self.assertIn('posts', response.context)
        self.assertTrue(Post.objects.all().count() == post_count)
        self.assertTrue(len(response.context['posts']) == published_count)
        self.assertQuerysetEqual(response.context['posts'], Post.objects.published(), transform=lambda x: x)
        html = response.content.decode('utf8')
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response, 'blog/post_list.html')
        
    def test_when_visited_by_superuser(self):
        '''
        ToDo:
            superuserのリクエストはすべての投稿を表示
            
        '''
        self.assertEqual(Post.objects.all().count(), 0)
        post_count = 5
        published_count = post_count - 2
        for i in range(post_count):
            post = create_post()
            post.title += f' {str(i)}'
            post.author = self.user
            if i < published_count: post.publish()
            post.save()
        
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.get('/')
        
        self.assertTrue(response.wsgi_request.user.is_superuser)        
        self.assertEqual(len(response.context['posts']), post_count)
        self.assertQuerysetEqual(response.context['posts'], Post.objects.all(), transform= lambda x:x)
      
      
    def test_get_posts_by_filtering_tag(self):
        '''
            query_stringにTagが指定された際は、そのTagと紐づいたPostのみ取得する。
        '''
        
        tag_names = ['Python', 'Ruby', 'Programming']
        for tag_name in tag_names:
            tag = create_tag(tag_name)
            tag.save()
            
        self.assertEquals(Tag.objects.all().count(), len(tag_names))
        
                
        posts = []
        for i in range(3):
            post = create_post()
            post.author = self.user
            post.publish()
            post.save()
            posts.append(post)
            
        tags = Tag.objects.all()    
        posts[0].tags.add(tags[0]) # Python
        
        posts[1].tags.add(tags[0]) # Python
        posts[1].tags.add(tags[2]) # Programming
        
        posts[2].tags.add(tags[1]) # Ruby
        posts[2].tags.add(tags[2]) # Programming
       
        [lambda post: post.save() for post in posts]
        
        response = self.client.get('/?tag=1')
        q_tag = response.wsgi_request.GET.get('tag', None)
        self.assertEqual(q_tag ,'1')
        
        tag = Tag.objects.get(pk=q_tag)
        self.assertEqual(tag.name, 'Python') # pkは１から
        self.assertEquals(response.context['posts'].count(), 2)
        
   
def create_tag(name):
    tag = Tag()
    tag.name = name
    return tag
        
def create_post():
    post = Post()
    post.title = 'sample post'
    post.content = 'sample content'
    return post

        
    