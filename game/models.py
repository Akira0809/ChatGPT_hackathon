from django.db import models

# Create your models here.
class Data(models.Model):
    questions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True) #データを追加した時間