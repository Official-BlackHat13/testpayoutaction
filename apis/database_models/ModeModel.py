from django.db import models
from datetime import datetime
import pytz
class ModeModel(models.Model):
    id = models.AutoField
    mode =models.CharField(max_length=300)
    created_at=models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Kolkata')))
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)