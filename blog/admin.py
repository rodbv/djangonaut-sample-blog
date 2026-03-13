from django.contrib import admin

from .models import Blog, Comment, Post


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_by", "created_at")
    list_filter = ("created_by",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("id", "created_at", "modified_at")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("id", "created_by", "created_at", "modified_at")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "blog", "slug", "created_by", "created_at")
    list_filter = ("blog", "created_by")
    search_fields = ("title", "slug", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("id", "created_at", "modified_at")
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "post", "created_by", "created_at")
    list_filter = ("post__blog", "created_by")
    search_fields = ("content",)
    readonly_fields = ("id", "created_at", "modified_at")
