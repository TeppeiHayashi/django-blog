from django.urls import resolve
from django.test import TestCase
from blog import views
from django.http.request import HttpRequest

class HomeViewTest(TestCase):
    
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, views.HomeView)
        
    def test_home_view_return_current_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!doctype html>'))
        self.assertIn('<title>Blog</title>', html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response, 'blog/home.html')
        
    