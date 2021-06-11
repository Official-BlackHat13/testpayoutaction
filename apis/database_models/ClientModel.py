from django.db import models

class ClientModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    client_code=models.CharField(max_length=60)
    auth_key=models.CharField(max_length=60)
    auth_iv=models.CharField(max_length=60)
    bank=models.IntegerField()
    def __str__(self):
        return str(self.id)