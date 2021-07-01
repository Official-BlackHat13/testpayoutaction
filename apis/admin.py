from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.MerchantModel)
admin.site.register(models.BankPartnerModel)
admin.site.register(models.LedgerModel)
admin.site.register(models.ChargeModel)
admin.site.register(models.FeatureModel)
admin.site.register(models.RoleModel)
admin.site.register(models.RoleFeatureModel)
admin.site.register(models.ModeModel)
admin.site.register(models.IpWhiteListedModel)
admin.site.register(models.IpHittingRecordModel)
admin.site.register(models.LogModel)