# Generated by Django 3.2 on 2021-07-09 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_auto_20210708_1713'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SlabModel',
        ),
        migrations.AddField(
            model_name='ledgermodel',
            name='payout_trans_id',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='ledgermodel',
            name='purpose',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 10, 975554)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839), null=True),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_amount_type',
            field=models.CharField(default='credited', max_length=20),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 904467)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 904467)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 888839)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 32, 9, 904467)),
        ),
    ]