from django.db import models

from datetime import datetime
class ChargeModel(models.Model):
    id=models.AutoField
    # client=models.IntegerField()
    mode=models.IntegerField()
    min_amount=models.IntegerField()
    max_amount=models.IntegerField()
    charge_percentage_or_fix=models.CharField(max_length=300)
    charge=models.IntegerField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None,null=True)
    updated_at=models.DateTimeField(default=None,null=True)
    merchant_id=models.IntegerField()
    def __str__(self):
        return str(self.id)
    
    