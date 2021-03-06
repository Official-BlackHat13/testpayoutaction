# Generated by Django 3.2 on 2021-07-26 06:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0023_auto_20210723_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bousermodel',
            old_name='role',
            new_name='role_id',
        ),
        migrations.RenameField(
            model_name='chargemodel',
            old_name='mode',
            new_name='mode_id',
        ),
        migrations.RenameField(
            model_name='ipwhitelistedmodel',
            old_name='merchant',
            new_name='merchant_id',
        ),
        migrations.RenameField(
            model_name='merchantmodel',
            old_name='bank',
            new_name='bank_id',
        ),
        migrations.RenameField(
            model_name='merchantmodel',
            old_name='client',
            new_name='client_id',
        ),
        migrations.RenameField(
            model_name='merchantmodel',
            old_name='role',
            new_name='role_id',
        ),
        migrations.RenameField(
            model_name='otpmodel',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='rolefeaturemodel',
            old_name='feature',
            new_name='feature_id',
        ),
        migrations.RenameField(
            model_name='rolefeaturemodel',
            old_name='role',
            new_name='role_id',
        ),
        migrations.RenameField(
            model_name='transactionhistorymodel',
            old_name='merchant',
            new_name='merchant_id',
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 22, 845555)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 133018)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 133018)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 24002)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 22, 977115)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 46149)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 77418)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 22, 845555)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 77418)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 93049)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 61789)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 61789)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 146031)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 22, 923708)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='trans_init_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 22, 923708)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 11, 40, 23, 111678)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 7, 26, 11, 40, 23, 161665)),
        ),
    ]
