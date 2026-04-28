from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from stories.models import Story, Bookmark


# 🔐 ĐĂNG KÝ
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'member'  # 👈 mặc định member
            user.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


# 👤 PROFILE
@login_required
def profile(request):
    # ❤️ truyện đã lưu
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('story').order_by('-created_at')

    # 📚 truyện đã đăng (nếu uploader)
    uploaded_stories = Story.objects.all().order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'bookmarks': bookmarks,
        'uploaded_stories': uploaded_stories,
    })