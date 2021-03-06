# Generated by Django 3.2.4 on 2021-07-16 05:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0010_auto_20210715_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 226175, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 268401, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 248301, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 228197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 228197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 238255, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 228197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 228197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 246278, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 218150, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 238255, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 248301, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 238255, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 238255, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 268401, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 16, 5, 26, 12, 248301, tzinfo=utc)),
        ),
    ]
