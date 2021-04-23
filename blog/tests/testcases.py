from django.test import TestCase
from django.contrib.auth.models import User


class CustomTestCase(TestCase):
    '''
        superuserを用いるTestCase
    '''

    def setUp(self):
        '''
            TestCase.setUp をオーバーライド。
            各テストメソッド前に実行される。
        '''
        if hasattr(self, 'user'):
            return

        self.username = 'test_admin1'
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user
