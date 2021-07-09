from django.db import models
from datetime import datetime
class LedgerModel(models.Model):
    id=models.AutoField
    merchant=models.IntegerField()
    client_code=models.CharField(max_length=60)
    amount=models.FloatField()
    trans_type=models.CharField(max_length=20) #payout/payin/charge
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
    created_at=models.DateTimeField(default=datetime.now(),null=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    createdBy= models.CharField(max_length=20,default=None,null=True)
    updatedBy = models.CharField(max_length=20,default=None,null=True)
    deletedBy = models.CharField(max_length=20, default=None, null=True)
    status = models.CharField(max_length=20,default=True)
    
    trans_amount_type = models.CharField(max_length=20,default="credited")
    # linked_ledger_id = models.CharField(max_length=20,null=True)
    # remarks = models.CharField(max_length=50,null=True)
    # status_code = models.IntegerField(default=0, null=True)
    # system_remarks = models.CharField(max_length=50,null=True)


    # trans_amount_type = models.CharField(max_length=20)
    # remarks = models.CharField(max_length=9000)

    # trans_amount_type = models.CharField(max_length=20)
    remarks = models.CharField(max_length=900,default="remarks")
    linked_ledger_id=models.IntegerField(null=True)
    status_code = models.CharField(null=True,max_length=900)
    system_remarks=models.CharField(null=True,max_length=900)
    payout_trans_id=models.CharField(max_length=100,default=None)
    purpose=models.CharField(max_length=1000,null=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.id)
