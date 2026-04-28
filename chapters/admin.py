from django.contrib import admin
from .models import Chapter, ChapterImage, Comment


# 🔥 Inline ảnh trong Chapter
class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    extra = 1


# 🔥 Admin Chapter (có sửa / xóa / tìm kiếm)
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('story', 'chapter_number', 'title')
    list_filter = ('story',)
    search_fields = ('title', 'story__title')
    ordering = ('story', 'chapter_number')
    inlines = [ChapterImageInline]


# 🔥 Admin Comment (để quản lý comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'created_at')
    search_fields = ('user__username', 'chapter__title', 'content')
    list_filter = ('created_at',)