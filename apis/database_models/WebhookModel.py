from django.db import models

from datetime import datetime

class WebhookModel(models.Model):
    id=models.AutoField
    merchant_id=models.IntegerField()
    webhook=models.CharField(max_length=2000)
    created_at=models.DateTimeField(datetime.now())
    status=models.BooleanField(default=True)
    updated_at=models.DateTimeField(default=None,null=True)
    deleted_at=models.DateTimeField(default=None,null=True)
    created_by=models.CharField(max_length=3000)
    updated_by=models.CharField(max_length=3000,default=None,null=True)
    deleted_by=models.CharField(max_length=3000,default=None,null=True)
    def __str__(self):
        return str(self.id)