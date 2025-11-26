from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.conf import settings
from .models import Post, Category, Tag, Comment


def post_list(request):
    """Homepage - list all published posts"""
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Trang chủ',
    }
    return render(request, 'blog_app/post_list.html', context)


def post_detail(request, slug):
    """Single post detail page"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments'),
        slug=slug,
        status='published'
    )
    
    # Increment views
    post.views += 1
    post.save(update_fields=['views'])
    
    # Get all comments
    comments = post.comments.all().order_by('-created_at')
    
    # Handle comment submission
    if request.method == 'POST':
        author_name = request.POST.get('author_name', '').strip()
        author_email = request.POST.get('author_email', '').strip()
        content = request.POST.get('content', '').strip()
        
        if author_name and author_email and content:
            Comment.objects.create(
                post=post,
                author_name=author_name,
                author_email=author_email,
                content=content,
                is_approved=True
            )
            return redirect('blog_app:post_detail', slug=slug)
    
    # Related posts
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'title': post.title,
    }
    return render(request, 'blog_app/post_detail.html', context)


def category_posts(request, slug):
    """Posts filtered by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category).select_related('author', 'category')
    
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'title': f'Danh mục: {category.name}',
    }
    return render(request, 'blog_app/category_posts.html', context)


def tag_posts(request, slug):
    """Posts filtered by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='published', tags=tag).select_related('author', 'category')
    
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tag': tag,
        'title': f'Thẻ: {tag.name}',
    }
    return render(request, 'blog_app/tag_posts.html', context)


def search(request):
    """Search posts by title and content"""
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query),
            status='published'
        ).select_related('author', 'category')
    
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'title': f'Tìm kiếm: {query}' if query else 'Tìm kiếm',
    }
    return render(request, 'blog_app/search.html', context)


def about(request):
    """About page"""
    context = {
        'title': 'Giới thiệu',
    }
    return render(request, 'blog_app/about.html', context)
