from email.policy import default
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="users")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user} has posted: {self.body}"

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="Liked")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} Likes {self.post}"        