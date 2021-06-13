from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ClientModel)
admin.site.register(models.BankModel)
admin.site.register(models.LedgerModel)
admin.site.register(models.ChargeModel)
admin.site.register(models.FeatureModel)
admin.site.register(models.RoleModel)
admin.site.register(models.RoleFeatureModel)
admin.site.register(models.ModeModel)