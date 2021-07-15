from django.db import models
from datetime import datetime


class BOUserModel(models.Model):
    id=models.AutoField
    role=models.IntegerField()
    username=models.CharField(max_length=300)
    password=models.CharField(max_length=300)
    name=models.CharField(max_length=300)
    email=models.EmailField(default=None,null=True)
    mobile=models.CharField(max_length=300)
    auth_key=models.CharField(max_length=300)
    auth_iv=models.CharField(max_length=300)
    created_at=models.DateTimeField(default=datetime.now())
    updated_at=models.DateTimeField(default=None,null=True)
    deleted_at=models.DateTimeField(default=None,null=True)
    created_by=models.CharField(max_length=300,null=True,default=None)
    updated_by=models.CharField(null=True,default=None,max_length=300)
    deleted_by=models.CharField(null=True,default=None,max_length=300)
    is_encrypt=models.BooleanField(default=True)
    def __str__(self):
        return str(self.id)
