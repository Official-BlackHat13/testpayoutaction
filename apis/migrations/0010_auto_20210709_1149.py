# Generated by Django 3.2 on 2021-07-09 06:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0009_auto_20210709_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlabModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_id', models.CharField(max_length=3000)),
                ('min_amount', models.IntegerField()),
                ('max_amount', models.IntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 267339))),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.DateTimeField(default=None, null=True)),
                ('deleted_by', models.DateTimeField(default=None, null=True)),
                ('updated_by', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 204839)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 36, 325430)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 204839)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 204839)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 220464)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 204839), null=True),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 204839)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 220464)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 189214)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 220464)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 236088)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 220464)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 220464)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 11, 49, 35, 236088)),
        ),
    ]
