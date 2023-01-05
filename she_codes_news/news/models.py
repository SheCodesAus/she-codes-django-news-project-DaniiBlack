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
    image_url = models.URLField(max_length=1000, default="https://picsum.photos/600")
    favourited_by = models.ManyToManyField(
        User, related_name="favourites", blank=True
    )
    categories = models.CharField(max_length=20, choices=[('clickbait','Clickbait'), ('politics','Politics'), ('travel','Travel'), ('badbitch', 'Bad bitch, its a genre')], default='Clickbait')

class Comment(models.Model):
    story = models.ForeignKey(NewsStory, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name="comments" ,on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)