# Generated by Django 3.2.4 on 2021-07-06 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0029_auto_20210703_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('user_type', models.CharField(max_length=1000)),
                ('verification_token', models.CharField(max_length=60)),
                ('mobile', models.CharField(max_length=12, null=True)),
                ('email', models.EmailField(max_length=1000)),
                ('otp', models.BigIntegerField()),
                ('expire_datetime', models.DateTimeField()),
                ('otp_status', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 616993))),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.DateTimeField(default=None, null=True)),
                ('deleted_by', models.DateTimeField(default=None, null=True)),
                ('updated_by', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserActiveModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_id', models.IntegerField()),
                ('tab_token', models.CharField(max_length=300)),
                ('active_status', models.CharField(max_length=300)),
                ('login_status', models.CharField(max_length=300)),
                ('client_ip_address', models.CharField(max_length=300)),
                ('tab_token_expire_time', models.DateTimeField(null=True)),
                ('geo_location', models.CharField(max_length=3000)),
                ('login_time', models.DateTimeField()),
                ('login_expire_time', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 618995))),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.DateTimeField(default=None, null=True)),
                ('deleted_by', models.DateTimeField(default=None, null=True)),
                ('updated_by', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='rolemodel',
            name='create',
        ),
        migrations.RemoveField(
            model_name='rolemodel',
            name='delete',
        ),
        migrations.RemoveField(
            model_name='rolemodel',
            name='read',
        ),
        migrations.RemoveField(
            model_name='rolemodel',
            name='update',
        ),
        migrations.AddField(
            model_name='featuremodel',
            name='created_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='featuremodel',
            name='deleted_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='featuremodel',
            name='updated_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='merchantmodel',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='rolefeaturemodel',
            name='created_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='rolefeaturemodel',
            name='custom_json',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='rolefeaturemodel',
            name='deleted_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='rolefeaturemodel',
            name='updated_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='rolemodel',
            name='created_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='rolemodel',
            name='deleted_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='rolemodel',
            name='permited_apis',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='rolemodel',
            name='updated_by',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 599007)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 605004)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 603005)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 608003)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 601007)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 601007)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 615001)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 597010)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 612999)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 612000)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 6, 15, 26, 50, 609997)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
