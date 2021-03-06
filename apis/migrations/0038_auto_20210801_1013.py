# Generated by Django 3.2 on 2021-08-01 04:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0037_auto_20210801_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372)),
        ),
        migrations.AlterField(
            model_name='dailyledgermodel',
            name='deleted_by',
            field=models.CharField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='dailyledgermodel',
            name='updated_by',
            field=models.CharField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 333821)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 333821)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 333821)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 333821)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='credit_transaction_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 318372), null=True),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 8, 1, 10, 13, 56, 340039)),
        ),
    ]
