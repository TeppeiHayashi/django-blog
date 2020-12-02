'''
    Modelに関するテストモジュール
'''

from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Post, Tag
from blog.tests.testcases import CustomTestCase


class PostModelTest(CustomTestCase):
     
    def test_create_and_get_post_object(self):
        '''
        ToDo:
            - 初期Post数は0 
            - Save後は1
            - 作成したオブジェクトとモデルから取得したPostオブジェクトが等しい。
        '''
        self.assertEquals(Post.objects.all().count(), 0)
        post = Post()
        post.title = 'sample post title'
        post.author = self.user
        post.content = 'sample post content'
        post.save()
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.get(pk=post.pk), post)

    def test_get_only_published_posts(self):
        self.assertEquals(Post.objects.all().count(), 0)
        
        for i in range(2):
            post = Post()
            post.title = 'sample post title'
            post.author = self.user
            post.content = 'sample post content'
            if i == 0: post.publish()
            post.save()     
        
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(Post.objects.published().count(), 1)
        

    def test_can_not_create_post_object_without_author(self):
        '''
        ToDo:
            ・authorなしでPostは投稿できない。
            ・ログイン済みのユーザでなければPostを投稿できない。
        '''
        post = Post()
        post.title = 'sample post title'
        post.content = 'sample post content'
        
        try: 
            post.save()
        except Exception as e:
            self.assertEquals(str(e.__cause__), 'NOT NULL constraint failed: blog_post.author_id')
            

        post.author = User()
        
        try:
            post.save()
        except Exception as e:
            self.assertEquals(e.__cause__, None)
            
 
class TagModelTest(TestCase):
 
    def test_not_insert_same_name(self):
        '''
            同一のnameを持つオブジェクトは追加できない。
        '''
        try:
            for i in range(2):
                tag = Tag()
                tag.name = 'Python'
                tag.save()
        except Exception as e:
            self.assertEquals(str(e.__cause__), 'UNIQUE constraint failed: blog_tag.name')
        
class UserModelTest(CustomTestCase):
    '''
        superuserを作成する。
        superuserでログインする。
        
    '''

    def test_is_superuser(self):
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.get('/')
        self.assertTrue(self.user.is_superuser)
        