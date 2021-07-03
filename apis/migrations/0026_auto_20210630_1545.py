# Generated by Django 3.2.4 on 2021-06-30 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0025_auto_20210629_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.CharField(max_length=300)),
                ('client_ip_address', models.CharField(max_length=100)),
                ('server_ip_address', models.CharField(max_length=100)),
                ('table_primary_id', models.IntegerField(null=True)),
                ('table_name', models.CharField(max_length=100, null=True)),
                ('remarks', models.CharField(max_length=100, null=True)),
                ('full_request', models.TextField(null=True)),
                ('full_response', models.TextField(null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 534896))),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.CharField(max_length=100, null=True)),
                ('updated_by', models.CharField(max_length=100, null=True)),
                ('deleted_by', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bankpartnermodel',
            name='created_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bankpartnermodel',
            name='deleted_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bankpartnermodel',
            name='updated_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 519281)),
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 519281)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 519281)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 534896)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='updated_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 519281)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_amount_type',
            field=models.CharField(default='cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 519281)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 519281)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='is_ip_checking',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 534896)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 534896)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 30, 15, 45, 26, 534896)),
        ),
    ]