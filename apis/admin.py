from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.MerchantModel)
admin.site.register(models.BankPartnerModel)
admin.site.register(models.TransactionHistoryModel)
admin.site.register(models.ChargeModel)
admin.site.register(models.FeatureModel)
admin.site.register(models.RoleModel)
admin.site.register(models.RoleFeatureModel)
admin.site.register(models.ModeModel)
admin.site.register(models.IpWhiteListedModel)
admin.site.register(models.IpHittingRecordModel)
admin.site.register(models.LogModel)
admin.site.register(models.OtpModel)
admin.site.register(models.BeneficiaryModel)
admin.site.register(models.UserActiveModel)
admin.site.register(models.BOUserModel)
admin.site.register(models.SlabModel)
admin.site.register(models.WebhookModel)
admin.site.register(models.MercahantModeModel)
admin.site.register(models.DailyLedgerModel)
