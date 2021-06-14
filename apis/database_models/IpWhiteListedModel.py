from django.db import models

class IpWhiteListedModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    client_code=models.CharField(max_length=300)
    ip_address=models.CharField(max_length=300)
    status=models.BooleanField()
    def __str__(self):
        return str(self.id)
