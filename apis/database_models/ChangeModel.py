from django.db import models

from datetime import datetime
class ChargeModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    mode=models.IntegerField()
    min_amount=models.IntegerField()
    max_amount=models.IntegerField()
    charge_percentage_or_fix=models.IntegerField()
    charge_amount_percentage=models.IntegerField()
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at=models.DateTimeField(default=None)
    updated_at=models.DateTimeField(default=None)
    def __str__(self):
        return str(self.id)
    
    