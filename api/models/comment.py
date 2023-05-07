from django.db import models
from django.utils import timezone
from api.models.lecture import Lecture
from hashids import Hashids
from api.models.user import CustomUser

from typing import (
    Any
)

class Comment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True, related_name="comments") # lecture idは自動で作られる
    commenter = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, related_name="comments")
    code = models.CharField(max_length=64, null=True)
    content = models.TextField(null=True)
    favo = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.code

    def save(self, force_insert: bool = False, force_update: bool = False, *args: Any, **kwargs: Any) -> None:
        super().save(force_insert, force_update, *args, **kwargs)
        if self.code is None:
            hashids = Hashids(
                min_length=5,
                alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                salt='lecture_comment'
            )
            self.code = f"LC_{hashids.encode(self.id)}"
            self.save()
