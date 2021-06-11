from django.db import models

class BankModel(models.Model):
    id=models.AutoField
    bank_name=models.CharField(max_length=100)
    bank_code=models.CharField(max_length=100)
    nodal_account_number=models.CharField(max_length=300)
    nodal_ifsc=models.CharField(max_length=300)
    nodal_account_name=models.CharField(max_length=300)
    def __str__(self):
        return str(self.id)