from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
]
