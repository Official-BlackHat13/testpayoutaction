from django.db import models


class ModeModel(models.Model):
    id = models.AutoField
    mode =models.CharField(max_length=300)