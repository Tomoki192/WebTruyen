from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Story, Category, Bookmark


def story_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort', 'new')

    stories = Story.objects.all()
    categories = Category.objects.all()

    # 🔎 Tìm kiếm
    if query:
        stories = stories.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    # 🏷 Lọc thể loại
    if category_id:
        stories = stories.filter(categories__id=category_id)

    # 🔥 Sắp xếp
    if sort == 'old':
        stories = stories.order_by('created_at')
    else:
        stories = stories.order_by('-created_at')

    # 📄 Phân trang
    paginator = Paginator(stories, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔥 TRUYỆN ĐỀ CỬ
    recommended_stories = Story.objects.order_by('-created_at')[:10]

    # ⭐ TOP TRUYỆN
    top_stories = Story.objects.order_by('-views')[:5]

    # 📈 TRENDING
    trending_stories = Story.objects.order_by('-views', '-created_at')[:5]

    return render(request, 'stories/list.html', {
        'stories': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'category_id': category_id,
        'sort': sort,
        'recommended_stories': recommended_stories,
        'top_stories': top_stories,
        'trending_stories': trending_stories,
    })


def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    # 🔥 TĂNG VIEW
    story.views += 1
    story.save(update_fields=['views'])

    chapters = story.chapters.all().order_by('chapter_number')

    # ❤️ CHECK BOOKMARK
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user,
            story=story
        ).exists()

    return render(request, 'stories/detail.html', {
        'story': story,
        'chapters': chapters,
        'is_bookmarked': is_bookmarked,
    })


@login_required
def toggle_bookmark(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        story=story
    )

    if not created:
        bookmark.delete()

    return redirect('story_detail', story_id=story.id)


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('story').order_by('-created_at')

    return render(request, 'stories/bookmarks.html', {
        'bookmarks': bookmarks
    })


@login_required
def create_story(request):
    if request.user.role != 'uploader':
        return HttpResponse("Bạn không có quyền đăng truyện")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        cover = request.FILES.get('cover')

        Story.objects.create(
            title=title,
            description=description,
            author=author,
            cover=cover
        )

        return redirect('home')

    return render(request, 'stories/create.html')


# 🔥 SỬA TRUYỆN
@login_required
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.user.role != 'uploader':
        return HttpResponse("Bạn không có quyền sửa")

    if request.method == 'POST':
        story.title = request.POST.get('title')
        story.description = request.POST.get('description')
        story.author = request.POST.get('author')

        if request.FILES.get('cover'):
            story.cover = request.FILES.get('cover')

        story.save()
        return redirect('story_detail', story_id=story.id)

    return render(request, 'stories/edit.html', {
        'story': story
    })


# 🔥 XÓA TRUYỆN
@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.user.role != 'uploader':
        return HttpResponse("Bạn không có quyền xóa")

    story.delete()
    return redirect('home')