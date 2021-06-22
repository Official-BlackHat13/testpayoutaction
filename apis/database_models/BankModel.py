from django.db import models
from datetime import datetime
class BankModel(models.Model):
    id=models.AutoField
    bank_name=models.CharField(max_length=100)
    bank_code=models.CharField(max_length=100)
    nodal_account_number=models.CharField(max_length=300)
    nodal_ifsc=models.CharField(max_length=300)
    nodal_account_name=models.CharField(max_length=300)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None)
    updated_at=models.DateTimeField(default=None)
    def __str__(self):
        return str(self.id)