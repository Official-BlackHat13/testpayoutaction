# Generated by Django 3.2.4 on 2021-06-30 04:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0025_auto_20210628_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 656435)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='clientmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 656435)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_amount_type',
            field=models.CharField(default='cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 10, 15, 27, 672082)),
        ),
    ]