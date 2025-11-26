from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    """Blog post category"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog_app:category', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Blog post tag"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Tên thẻ")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    
    class Meta:
        verbose_name = "Thẻ"
        verbose_name_plural = "Thẻ"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog_app:tag', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog post"""
    STATUS_CHOICES = [
        ('draft', 'Bản nháp'),
        ('published', 'Đã xuất bản'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Tác giả")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name="Danh mục")
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Thẻ")
    
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="Tóm tắt")
    content = models.TextField(verbose_name="Nội dung")
    featured_image = models.ImageField(upload_to='posts/%Y/%m/', blank=True, null=True, verbose_name="Ảnh đại diện")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Trạng thái")
    views = models.PositiveIntegerField(default=0, verbose_name="Lượt xem")
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày xuất bản")
    
    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_app:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        if not self.excerpt:
            self.excerpt = self.content[:200] + '...' if len(self.content) > 200 else self.content
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Blog post comment"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Bài viết")
    author_name = models.CharField(max_length=100, verbose_name="Tên")
    author_email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_approved = models.BooleanField(default=False, verbose_name="Đã duyệt")
    
    class Meta:
        verbose_name = "Bình luận"
        verbose_name_plural = "Bình luận"
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Bình luận bởi {self.author_name} trên {self.post.title}'
