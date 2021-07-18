from django.db import models

from datetime import datetime

class BeneficiaryModel(models.Model):
    id=models.AutoField
    full_name=models.CharField(max_length=3000)
    account_number=models.CharField(max_length=400)
    ifsc_code=models.CharField(max_length=500)
    merchant_id=models.IntegerField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    created_by=models.CharField(max_length=30,default="merchant")
    deleted_by=models.DateTimeField(default=None,null=True)
    updated_by=models.CharField(max_length=20,null=True)
    def __str__(self):
        return str(self.id)