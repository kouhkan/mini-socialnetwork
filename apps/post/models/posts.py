from django.contrib.auth.models import User
from django.db import models

from core.base_models import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.title[:10]}"
