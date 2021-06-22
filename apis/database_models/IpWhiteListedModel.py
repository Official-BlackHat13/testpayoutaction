from django.db import models
from datetime import datetime
class IpWhiteListedModel(models.Model):
    id=models.AutoField
    client_model=models.IntegerField()
    ip_address=models.CharField(max_length=300)
    status=models.BooleanField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None)
    updated_at=models.DateTimeField(default=None)
    def __str__(self):
        return str(self.id)
