from django.db import models

from datetime import datetime

class SlabModel(models.Model):
    id=models.AutoField
    merchant_id=models.CharField(max_length=3000)
    min_amount=models.IntegerField()
    max_amount=models.IntegerField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.DateTimeField(default=None,null=True)
    deleted_by=models.DateTimeField(default=None,null=True)
    updated_by=models.DateTimeField(default=None,null=True)
    status=models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)