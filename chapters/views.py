from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from stories.models import Story
from .models import Chapter, Comment, ChapterImage


def chapter_detail(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)

    # 🔁 Chapter trước / sau
    prev_chapter = Chapter.objects.filter(
        story=chapter.story,
        chapter_number__lt=chapter.chapter_number
    ).order_by('-chapter_number').first()

    next_chapter = Chapter.objects.filter(
        story=chapter.story,
        chapter_number__gt=chapter.chapter_number
    ).order_by('chapter_number').first()

    # 📚 Danh sách chapter
    all_chapters = Chapter.objects.filter(
        story=chapter.story
    ).order_by('chapter_number')

    # 💬 Xử lý comment
    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('content')
            if content:
                Comment.objects.create(
                    user=request.user,
                    chapter=chapter,
                    content=content
                )
        return redirect('chapter_detail', chapter_id=chapter.id)

    comments = chapter.comments.all().order_by('-created_at')

    return render(request, 'chapters/detail.html', {
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'all_chapters': all_chapters,
        'comments': comments,
    })


@login_required
def create_chapter(request):
    if request.user.role != 'uploader':
        return HttpResponse("Bạn không có quyền đăng chapter")

    stories = Story.objects.all()

    if request.method == 'POST':
        story_id = request.POST.get('story')
        title = request.POST.get('title')
        content = request.POST.get('content')
        chapter_number = request.POST.get('chapter_number')

        story = get_object_or_404(Story, id=story_id)

        # 🔥 tạo chapter
        chapter = Chapter.objects.create(
            story=story,
            title=title,
            content=content,
            chapter_number=chapter_number
        )

        # 🔥 upload nhiều ảnh
        images = request.FILES.getlist('images')
        for img in images:
            ChapterImage.objects.create(
                chapter=chapter,
                image=img
            )

        return redirect('chapter_detail', chapter_id=chapter.id)

    return render(request, 'chapters/create.html', {
        'stories': stories
    })


# ✏️ EDIT CHAPTER
@login_required
def edit_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)

    if request.user.role != 'uploader':
        return HttpResponse("Bạn không có quyền sửa chapter")

    if request.method == 'POST':
        chapter.title = request.POST.get('title')
        chapter.chapter_number = request.POST.get('chapter_number')
        chapter.content = request.POST.get('content')
        chapter.save()

        # thêm ảnh mới
        images = request.FILES.getlist('images')
        for img in images:
            ChapterImage.objects.create(
                chapter=chapter,
                image=img
            )

        return redirect('chapter_detail', chapter_id=chapter.id)

    return render(request, 'chapters/edit.html', {
        'chapter': chapter
    })


# ❌ DELETE CHAPTER
@login_required
def delete_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    story_id = chapter.story.id

    if request.user.role != 'uploader':
        return HttpResponse("Bạn không có quyền xóa chapter")

    if request.method == 'POST':
        chapter.delete()
        return redirect('story_detail', story_id=story_id)

    return render(request, 'chapters/delete.html', {
        'chapter': chapter
    })