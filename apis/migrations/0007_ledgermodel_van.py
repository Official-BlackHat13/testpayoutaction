# Generated by Django 3.2 on 2021-06-13 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0006_ledgermodel_trans_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledgermodel',
            name='van',
            field=models.CharField(default='000000000', max_length=200),
            preserve_default=False,
        ),
    ]