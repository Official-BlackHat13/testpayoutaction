from django.db import models

class LedgerModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    client_code=models.CharField(max_length=60)
    amount=models.FloatField()
    trans_type=models.CharField(max_length=20)
    type_status=models.CharField(max_length=60)
    bank_ref_no=models.CharField(max_length=1000)
    customer_ref_no=models.CharField(max_length=1000)
    bank=models.IntegerField()
    trans_status=models.CharField(max_length=100)
    bene_account_name=models.CharField(max_length=300)
    bene_account_number=models.CharField(max_length=300)
    bene_ifsc=models.CharField(max_length=300)
    request_header=models.CharField(max_length=400)
    mode=models.IntegerField()
    charge=models.FloatField()
    trans_time=models.DateTimeField()
    van=models.CharField(max_length=200)
    def __str__(self):
        return str(self.id)
