# Generated by Django 3.2.4 on 2021-10-27 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0079_auto_20211020_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 189287)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 189287)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
        migrations.AlterField(
            model_name='taxmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 241681)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 204911)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 27, 15, 6, 12, 220533)),
        ),
    ]