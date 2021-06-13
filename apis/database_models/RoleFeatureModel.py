from django.db import models

class RoleFeatureModel(models.Model):
    id=models.AutoField
    role=models.IntegerField()
    feature=models.IntegerField()
    
    def __str__(self):
        return str(self.id)