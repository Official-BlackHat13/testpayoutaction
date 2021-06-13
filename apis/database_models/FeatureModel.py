from django.db import models
class FeatureModel(models.Model):
    id=models.AutoField
    feature_name=models.CharField(max_length=300)
    slug=models.CharField(max_length=100)