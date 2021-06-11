from django.db import models

class LedgerModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    client_code=models.CharField(max_length=60)
    amount=models.IntegerField()
    trans_type=models.CharField(max_length=20)
    status=models.CharField(max_length=60)
    bank_ref_no=models.CharField(max_length=1000)
    customer_ref_no=models.CharField(max_length=1000)
    bank=models.ImageField()
    trans_time=models.DateTimeField()
    def __str__(self):
        return str(self.id)
