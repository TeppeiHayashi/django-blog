from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('comment/create/<int:pk>/',
         views.CreateComment.as_view(), name='add_comment'),
    path('reply/create/<int:pk>/', views.CreateReply.as_view(), name='add_reply'),
    path('archive/tag/<str:name>',
         views.TagPostListView.as_view(), name='tag_post_list')
]
