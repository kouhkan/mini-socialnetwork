from django.contrib.auth.models import User
from django.db import models

from apps.post.models import Post
from core.base_models import BaseModel


class Rate(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rates")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="rates")
    rate = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (
            ("user", "post"),
        )

    def __str__(self) -> str:
        return f"{self.user} - {self.rate}"
