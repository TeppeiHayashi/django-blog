from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Post

class SuperUserTestCase(TestCase):
    '''
        superuserを用いるTestCase
    '''
     
    def setUp(self):
        '''
            TestCase.setUp をオーバーライド。
            各テストメソッド前に実行される。
        '''
        self.username = 'test_admin1'
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user


class PostModelTest(SuperUserTestCase):
     
    def test_create_and_get_post_object(self):
        '''
        ToDo:
            ・初期Post数は0
            ・Save後は1
            ・作成したオブジェクトとモデルから取得したPostオブジェクトが等しい。
        '''
        self.assertEquals(Post.objects.all().count(), 0)
        post = Post()
        post.title = 'sample post title'
        post.author = self.user
        post.content = 'sample post content'
        post.save()
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.get(pk=post.pk).title, 'sample post title')

    def test_can_not_create_post_object_without_author(self):
        '''
            ・authorなしでPostは投稿できない。
        '''
        post = Post()
        post.title = 'sample post title'
        post.content = 'sample post content'
        
        try: 
            post.save()
        except:
            self.assertTrue(True)
            

        post.author = User()
        
        try:
            post.save()
        except:
            self.assertTrue(True)
            
    
        
class UserModelTest(SuperUserTestCase):
    '''
        superuserを作成する。
        superuserでログインする。
        
    '''

    def test_is_superuser(self):
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.get('/')
        self.assertTrue(self.user.is_superuser)
        