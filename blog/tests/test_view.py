from django.urls import resolve
from django.test import TestCase
from blog import views

class HomePage(TestCase):
    
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, views.HomeView)