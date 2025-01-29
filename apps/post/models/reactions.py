from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.post.models import Post
from core.base_models import BaseModel


class ReactionStatusChoices(models.TextChoices):
    LIKE = _("like"), "LIKE"
    DISLIKE = _("dislike"), "DISLIKE"


class Reaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.CharField(max_length=7, choices=ReactionStatusChoices.choices)

    class Meta:
        unique_together = (
            ("user", "post"),
        )

    def __str__(self) -> str:
        return f"{self.user} - {self.reaction}"
