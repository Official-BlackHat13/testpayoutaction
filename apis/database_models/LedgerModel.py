from django.db import models
from datetime import datetime
class LedgerModel(models.Model):
    id=models.AutoField
    merchant=models.IntegerField()
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
    mode=models.IntegerField()
    request_header=models.CharField(max_length=400)
    charge=models.FloatField()
    trans_time = models.DateTimeField(default=datetime.now())
    van=models.CharField(max_length=200)
    created_at=models.DateTimeField(default=datetime.now())
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    createdBy= models.CharField(max_length=20,default=None)
    updatedBy = models.CharField(max_length=20,default=None,null=True)
    deletedBy = models.CharField(max_length=20, default=None, null=True)
    status = models.CharField(max_length=20,default=True)
<<<<<<< HEAD
    trans_amount_type = models.CharField(max_length=20,default="credit")
    linked_ledger_id = models.CharField(max_length=20,null=True)
    remarks = models.CharField(max_length=50,null=True)
    status_code = models.IntegerField(default=0, null=True)
    system_remarks = models.CharField(max_length=50,null=True)

=======
    trans_amount_type = models.CharField(max_length=20)
    remarks = models.CharField(max_length=9000)
>>>>>>> working
    objects = models.Manager()
    # def __str__(self):
    #     return str(self.id)
