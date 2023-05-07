from django.db import models
from django.utils import timezone
from typing import Any
from api.models.user import CustomUser
from api.models.lecture import Lecture

class LectureCustomer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name="lecture_customers")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=False, related_name="lecture_customers")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "lecture_customer"
