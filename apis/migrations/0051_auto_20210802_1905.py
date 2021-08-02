# Generated by Django 3.2 on 2021-08-02 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0050_auto_20210802_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 870059)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 870059)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 901319)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 870059)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 901319)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 870059)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='credit_transaction_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 870059), null=True),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='tax',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 885689)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 2, 19, 5, 47, 901319)),
        ),
    ]
