from django.db import models
from django.conf import settings
from stories.models import Story


class Chapter(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    chapter_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.story.title} - Chapter {self.chapter_number}: {self.title}"


class ChapterImage(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='chapters/')

    def __str__(self):
        return f"Image of {self.chapter.title}"


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chapter.title}"