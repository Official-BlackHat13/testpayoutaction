# Generated by Django 3.2 on 2021-07-06 19:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0041_auto_20210707_0022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chargemodel',
            old_name='charge_amount_percentage',
            new_name='charge',
        ),
        migrations.AddField(
            model_name='chargemodel',
            name='merchant_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 966419)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='charge_percentage_or_fix',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 997674)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 966419)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 997674)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 966419)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 966419)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 39, 13297)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 959900)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 39, 13297)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 39, 13297)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 39, 13297)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 38, 997674)),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 41, 78476)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 0, 34, 39, 13297)),
        ),
    ]
