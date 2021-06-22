from django.db import models
from datetime import datetime
class ClientModel(models.Model):
    id=models.AutoField
    role=models.IntegerField()
    client=models.IntegerField()
    client_code=models.CharField(max_length=60)
    auth_key=models.CharField(max_length=60)
    auth_iv=models.CharField(max_length=60)
    bank=models.IntegerField()
    client_username=models.CharField(max_length=100)
    client_password=models.CharField(max_length=100)
    is_payout = models.BooleanField()
    is_merchant=models.BooleanField()
    status = models.BooleanField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None)
    updated_at=models.DateTimeField(default=None)
    def __str__(self):
        return str(self.id)