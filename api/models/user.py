from django.db import models
from django.utils import timezone

class CustomeUser(models.Model):
    name = models.CharField(max_length=128, null=True) 
    mail = models.TextField(null=True) 
    eoa = models.CharField(max_length=256) # user の wallet account address．
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "custom_user"
