# Generated by Django 3.2 on 2021-06-27 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0020_auto_20210627_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 971725)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 977725)),
        ),
        migrations.AlterField(
            model_name='clientmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 970725)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 976725)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 980726)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 974726)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 974726)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 985726)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 983726)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 27, 14, 22, 56, 981726)),
        ),
    ]