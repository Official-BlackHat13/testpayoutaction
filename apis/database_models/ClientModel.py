from django.db import models
from datetime import datetime
class ClientModel(models.Model):
    id=models.AutoField
    role=models.IntegerField(null=True)
    client=models.IntegerField()
    client_code=models.CharField(max_length=60)
    auth_key=models.CharField(max_length=60)
    auth_iv=models.CharField(max_length=60)
    bank=models.IntegerField()
    client_username=models.CharField(max_length=100)
    client_password=models.CharField(max_length=100)
    is_payout = models.BooleanField(null=True)
    is_merchant=models.BooleanField(null=True)
    status = models.BooleanField(default=True)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    user = models.IntegerField()
    def __str__(self):
        return str(self.id)