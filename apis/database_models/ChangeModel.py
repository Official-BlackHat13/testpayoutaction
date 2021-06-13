from django.db import models


class ChargeModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    mode=models.IntegerField()
    min_amount=models.IntegerField()
    max_amount=models.IntegerField()
    charge_percentage_or_fix=models.IntegerField()
    charge_amount_percentage=models.IntegerField()
    def __str__(self):
        return str(self.id)
    
    