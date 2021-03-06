# Generated by Django 3.2 on 2021-08-01 04:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0035_auto_20210731_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 7296)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 643408)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 574352)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 186966)),
        ),
        migrations.AlterField(
            model_name='dailyledgermodel',
            name='opening_balance',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 85468)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 226970)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 326809)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 747551)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 0, 953873)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 305120)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 404939)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 289490)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 258230)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 674667)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 54208)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='credit_transaction_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 54208), null=True),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 1, 9, 45, 1, 411474)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 8, 1, 9, 45, 1, 716276)),
        ),
    ]
