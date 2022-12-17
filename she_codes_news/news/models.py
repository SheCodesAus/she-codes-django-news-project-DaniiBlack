from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField()
    content = models.TextField()
    liked_by = models.ManyToManyField(User, related_name='liked_stories', blank=True)
    favourited_by = models.ManyToManyField(
        User, related_name="favourites", blank=True
    )

class Comment(models.Model):
    story = models.ForeignKey(NewsStory, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name="comments" ,on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)