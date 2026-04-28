from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Story(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    categories = models.ManyToManyField(Category)

    # 🔥 LƯỢT XEM
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ❤️ BOOKMARK (lưu truyện)
class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')  # ❗ không cho lưu trùng

    def __str__(self):
        return f"{self.user.username} ❤️ {self.story.title}"