from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ClientModel)
admin.site.register(models.BankModel)
admin.site.register(models.LedgerModel)