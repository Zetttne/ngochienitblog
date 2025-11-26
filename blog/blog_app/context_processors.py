from django.db.models import Count, Q
from .models import Category, Tag, Post


def blog_context(request):
    """Global context processor for blog"""
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0).order_by('name')
    
    popular_tags = Tag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0).order_by('-post_count')[:10]
    
    return {
        'site_name': 'Blog cá nhân Hiền Data',
        'recent_posts': Post.objects.filter(status='published').order_by('-published_at')[:5],
        'categories': categories,
        'popular_tags': popular_tags,
    }
