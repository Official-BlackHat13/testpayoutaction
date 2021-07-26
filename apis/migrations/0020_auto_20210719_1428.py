# Generated by Django 3.2 on 2021-07-19 08:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0019_auto_20210719_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant', models.IntegerField()),
                ('client_code', models.CharField(max_length=60)),
                ('amount', models.FloatField()),
                ('trans_type', models.CharField(max_length=20)),
                ('type_status', models.CharField(max_length=60)),
                ('bank_ref_no', models.CharField(max_length=1000)),
                ('customer_ref_no', models.CharField(max_length=1000)),
                ('bank_partner_id', models.IntegerField()),
                ('trans_status', models.CharField(max_length=100)),
                ('bene_account_name', models.CharField(max_length=300)),
                ('bene_account_number', models.CharField(max_length=300)),
                ('bene_ifsc', models.CharField(max_length=300)),
                ('payment_mode', models.IntegerField()),
                ('request_header', models.CharField(max_length=400)),
                ('charge', models.FloatField()),
                ('trans_init_time', models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 533201))),
                ('trans_completed_time', models.DateTimeField(null=True)),
                ('van', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 533201))),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('createdBy', models.CharField(default=None, max_length=20, null=True)),
                ('updatedBy', models.CharField(default=None, max_length=20, null=True)),
                ('deletedBy', models.CharField(default=None, max_length=20, null=True)),
                ('status', models.CharField(default=True, max_length=20)),
                ('trans_amount_type', models.CharField(default='credited', max_length=20)),
                ('remarks', models.CharField(default='remarks', max_length=900)),
                ('linked_Txn_id', models.IntegerField(null=True)),
                ('status_code', models.CharField(max_length=900, null=True)),
                ('system_remarks', models.CharField(max_length=900, null=True)),
                ('payout_trans_id', models.CharField(default=None, max_length=100)),
                ('purpose', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='TranstionHistoryModel',
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 530199)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 557202)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 555202)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 538201)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 536201)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 541201)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 549202)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 468194)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 547201)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 551202)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 545201)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 543201)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 559201)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 19, 14, 28, 30, 553202)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 7, 19, 14, 28, 30, 561202)),
        ),
    ]