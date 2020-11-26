from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from factory import LazyFunction, LazyAttribute, Sequence, Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from blog.models import Post, Tag
from factory.declarations import LazyFunction

UserModel = get_user_model()
FAKER_LOCALE = 'ja_JP'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
        
    username = Sequence(lambda n: f'user{n}')
    email = LazyAttribute(lambda o: f'{o.username}@example.com')
    is_staff = False
    is_active = True
    
class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = Sequence(lambda n: f'tag{n}')
 
class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        
    title = Faker('word', locale=FAKER_LOCALE)
    content = Faker('text', locale=FAKER_LOCALE)
    author = SubFactory(UserFactory)
    published_at = LazyFunction(timezone.now) # テストデータはデフォルトで公開済みとする。
    
    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
    
    