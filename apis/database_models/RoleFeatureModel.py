from django.db import models
from datetime import datetime
import pytz
class RoleFeatureModel(models.Model):
    id=models.AutoField
    role=models.IntegerField()
    feature=models.IntegerField()
    custom_json = models.CharField(max_length=300,default=None,null=True)
    created_at=models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Kolkata')))
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.DateTimeField(default=None,null=True)
    deleted_by=models.DateTimeField(default=None,null=True)
    updated_by=models.DateTimeField(default=None,null=True)
    def __str__(self):
        return str(self.id)