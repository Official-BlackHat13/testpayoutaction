# Generated by Django 3.2 on 2021-08-17 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0065_auto_20210817_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 749748)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 771750)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 769750)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 756749)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 755749)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 759750)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 764751)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 775750)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 747749)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 763749)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 766750)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 762750)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 760750)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 772751)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 751748)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 767751)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 12, 27, 42, 774751)),
        ),
    ]
