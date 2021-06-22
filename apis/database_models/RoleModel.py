from django.db import models

from datetime import datetime
class RoleModel(models.Model):
    id=models.AutoField
    role_name=models.CharField(max_length=300)
    create=models.BooleanField()
    read=models.BooleanField()
    update=models.BooleanField()
    delete=models.BooleanField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None)
    updated_at=models.DateTimeField(default=None)
    def __str__(self):
        return str(self.id)