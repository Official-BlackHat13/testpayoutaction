from django.db import models




class DailyLedgerModel(models.Model):
    id=models.AutoField
    merchant_id=models.IntegerField()
    date=models.DateField()
    opening_balance=models.IntegerField()
    closing_balance=models.IntegerField()
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField(null=True)
    deleted_at=models.DateTimeField(null=True)
    created_by=models.CharField(max_length=3000)
    updated_by=models.CharField(max_length=3000)
    deleted_by=models.CharField(max_length=3000)
    def __str__(self):
        return str(self.id)
    