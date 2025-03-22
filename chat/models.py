from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Image(models.Model):
    chat = models.ForeignKey(Chat, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chat_images/')
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Chat {self.chat.title}"
