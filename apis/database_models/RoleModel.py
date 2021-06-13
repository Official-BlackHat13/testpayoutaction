from django.db import models


class RoleModel(models.Model):
    id=models.AutoField
    role_name=models.CharField(max_length=300)
    create=models.BooleanField()
    read=models.BooleanField()
    update=models.BooleanField()
    delete=models.BooleanField()
    def __str__(self):
        return str(self.id)