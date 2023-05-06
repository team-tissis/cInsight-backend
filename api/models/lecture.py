from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from api.models.user import CustomUser

class Lecture(models.Model):
    name = models.TextField(null=True) 
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="lectures")
    from_date = models.DateTimeField(null=True) 
    to_date = models.DateTimeField(null=True) 
    tags = JSONField(null=True)
    description = models.TextField(null=True)
    material_url = models.URLField(null=True) # 資料 url
    movie_url = models.URLField(null=True) # 動画 url

    favo = models.IntegerField(null=True)
    attendee_max_num = models.IntegerField(null=True) # 参加上限数
    attendee_num = models.IntegerField(null=True) # 現在の参加者数
    attendee_eoas = JSONField(null=True) # userのwallet account addressのjson．"{"eoa":["0xhoge", "0xfuga"]}"

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lecture"
