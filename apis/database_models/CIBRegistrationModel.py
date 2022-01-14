from django.db import models
from datetime import datetime
import uuid

class CIBRegistration(models.Model):
    id=models.AutoField(primary_key=True)
    # bank = models.ForeignKey('BankModel', on_delete=models.CASCADE)
    aggrName = models.CharField(max_length=100, blank=True, null=True)
    aggrId = models.CharField(max_length=100, blank=True, null=True)
    corpId = models.CharField(max_length=100, blank=True, null=True)
    userId = models.CharField(max_length=100, blank=True, null=True)
    aliasId = models.CharField(max_length=100, blank=True, null=True)
    urn = models.CharField(null=False, max_length=50, default=uuid.uuid4)
    errorMessage = models.CharField(max_length=100, blank=True, null=True)
    response = models.CharField(max_length=100, blank=True, null=True)
    success = models.BooleanField(default=False, null = True)
    status = models.CharField(max_length=100, null = True)
    message = models.CharField(max_length=100, null = True)
    errorCode = models.CharField(max_length=100, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None,null=True)
    updated_at = models.DateTimeField(auto_now = True)


    # def __str__(self):
    #     return str(self.bank.bank_name)

