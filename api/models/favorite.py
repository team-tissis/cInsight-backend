from django.db import models
from django.utils import timezone
from typing import Any
from api.models.user import CustomeUser
from api.models.lecture import Lecture

class Favorite(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, null=False)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=False)
    is_synced = models.BooleanField(help_text='オンチェーンにデータを保存できたらTrue', default=False)
    vote_weight = models.IntegerField(default=1, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "favorite"
