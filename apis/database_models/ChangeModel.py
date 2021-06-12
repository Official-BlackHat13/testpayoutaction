from django.db import models


class ChargeModel(models.Model):
    id=models.AutoField
    client=models.IntegerField()
    mode=models.IntegerField()
    