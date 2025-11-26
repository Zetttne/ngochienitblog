from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['author_name', 'author_email', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    inlines = [CommentInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Nội dung', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Xuất bản', {
            'fields': ('status', 'published_at')
        }),
        ('Thống kê', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Duyệt bình luận đã chọn"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Bỏ duyệt bình luận đã chọn"
