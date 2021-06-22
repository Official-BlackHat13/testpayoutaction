from django.db import models
from datetime import datetime
class RoleFeatureModel(models.Model):
    id=models.AutoField
    role=models.IntegerField()
    feature=models.IntegerField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None)
    updated_at=models.DateTimeField(default=None)
    def __str__(self):
        return str(self.id)