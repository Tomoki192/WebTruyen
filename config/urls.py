from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# views
from stories.views import (
    story_list,
    story_detail,
    create_story,
    edit_story,
    delete_story,
    toggle_bookmark,   # ❤️ thêm
    my_bookmarks       # ❤️ thêm
)

from chapters.views import (
    chapter_detail,
    create_chapter,
    edit_chapter,
    delete_chapter
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('accounts/', include('accounts.urls')),

    # 🔥 STORY
    path('', story_list, name='home'),
    path('story/<int:story_id>/', story_detail, name='story_detail'),
    path('create-story/', create_story, name='create_story'),

    # ✏️ EDIT / DELETE STORY
    path('story/<int:story_id>/edit/', edit_story, name='edit_story'),
    path('story/<int:story_id>/delete/', delete_story, name='delete_story'),

    # ❤️ BOOKMARK
    path('story/<int:story_id>/bookmark/', toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', my_bookmarks, name='my_bookmarks'),

    # 📚 CHAPTER
    path('chapter/<int:chapter_id>/', chapter_detail, name='chapter_detail'),
    path('create-chapter/', create_chapter, name='create_chapter'),
    path('chapter/<int:chapter_id>/edit/', edit_chapter, name='edit_chapter'),
    path('chapter/<int:chapter_id>/delete/', delete_chapter, name='delete_chapter'),
]

# media (ảnh)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)